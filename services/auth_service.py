"""Authentication service for user management."""

import html
import logging
import os
import random
import re
import smtplib
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import url_for
from flask_login import login_user, logout_user
from sqlalchemy import func
from sqlalchemy.exc import OperationalError, IntegrityError

from models import db
from models.oauth_account import OAuthAccount
from models.user import User

logger = logging.getLogger(__name__)

_password_reset_cooldowns = {}
PASSWORD_RESET_COOLDOWN_SECONDS = int(os.environ.get("PASSWORD_RESET_COOLDOWN_SECONDS", "300"))


class OAuthLinkConflict(Exception):
    """Raised when an OAuth account is already linked to a different user."""


class OAuthNeedsLinking(Exception):
    """Raised when OAuth login finds an existing password-based account by email."""


class AuthService:
    MIN_PASSWORD_LENGTH = 8

    @staticmethod
    def validate_email(email):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email or "") is not None

    @staticmethod
    def validate_username(username):
        if not username or len(username) < 3 or len(username) > 80:
            return False, "Username must be between 3 and 80 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, None

    @staticmethod
    def validate_password(password):
        if not password or len(password) < AuthService.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {AuthService.MIN_PASSWORD_LENGTH} characters"
        return True, None

    @staticmethod
    def normalize_username(username):
        return (username or "").strip().lower()

    @staticmethod
    def normalize_email(email):
        return (email or "").strip().lower()

    @classmethod
    def sanitize_oauth_username(cls, username_hint: str, provider_prefix: str = "oauth") -> str:
        """Sanitize OAuth username to local username rules (letters/numbers/underscore)."""
        candidate = cls.normalize_username(username_hint)
        candidate = re.sub(r'[^a-z0-9_]+', '_', candidate)
        candidate = re.sub(r'_+', '_', candidate).strip('_')
        prefix = cls.normalize_username(provider_prefix) or "oauth"
        if len(candidate) < 3:
            candidate = f"{prefix}_{candidate}".strip('_')
        if len(candidate) < 3:
            candidate = f"{prefix}_user"
        return candidate[:80]

    @staticmethod
    def _run_db_retry(fn, retries=2):
        last_exc = None
        for attempt in range(retries):
            try:
                return fn()
            except OperationalError as exc:
                db.session.rollback()
                last_exc = exc
                logger.warning("Transient DB operational error (attempt %s/%s): %s", attempt + 1, retries, exc)
                time.sleep(0.3 * (attempt + 1))
        raise last_exc

    @classmethod
    def register_user(cls, username, email, password):
        try:
            normalized_username = cls.normalize_username(username)
            normalized_email = cls.normalize_email(email)

            valid, error = cls.validate_username(normalized_username)
            if not valid:
                return False, error
            if not cls.validate_email(normalized_email):
                return False, "Invalid email format"
            valid, error = cls.validate_password(password)
            if not valid:
                return False, error

            def _create_user():
                if User.query.filter(func.lower(User.username) == normalized_username).first():
                    return False, "Username already taken"
                if User.query.filter(func.lower(User.email) == normalized_email).first():
                    return False, "Email already registered"
                user = User(username=normalized_username, email=normalized_email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return True, user

            success, result = cls._run_db_retry(_create_user)
            if success:
                cls._dispatch_email(cls._send_welcome_email, result.email, result.username)
            return success, result
        except Exception as e:
            db.session.rollback()
            logger.exception("Registration failed")
            return False, f"Registration failed: {str(e)}"

    @staticmethod
    def authenticate_user(username_or_email, password):
        normalized_identifier = (username_or_email or "").strip().lower()
        user = User.query.filter(
            (func.lower(User.username) == normalized_identifier)
            | (func.lower(User.email) == normalized_identifier)
        ).first()
        if not user or not user.is_active:
            return False, "Invalid username/email or password"
        if not user.password_hash:
            return False, "This account uses GitHub login. Please sign in with GitHub."
        if not user.check_password(password):
            return False, "Invalid username/email or password"
        return True, user

    @staticmethod
    def login(user, remember=False):
        try:
            login_user(user, remember=remember)
            user.update_last_login()
            return True
        except Exception:
            return False

    @staticmethod
    def logout():
        logout_user()
        return True

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(int(user_id))

    @classmethod
    def initiate_password_reset(cls, email: str, client_ip: str = "unknown"):
        normalized_email = cls.normalize_email(email)
        if not normalized_email:
            return True, "If this email is registered, you will receive a password reset link."

        now = time.time()
        for key in (f"email:{normalized_email}", f"ip:{client_ip}"):
            last = _password_reset_cooldowns.get(key)
            if last and now - last < PASSWORD_RESET_COOLDOWN_SECONDS:
                return True, "If this email is registered, you will receive a password reset link shortly."
            _password_reset_cooldowns[key] = now

        user = User.query.filter(func.lower(User.email) == normalized_email).first()
        if not user or not user.is_active:
            return True, "If this email is registered, you will receive a password reset link."

        token = user.generate_reset_token()
        cls._dispatch_email(cls._send_reset_email, user.email, user.username, token)
        return True, "If this email is registered, you will receive a password reset link."

    @classmethod
    def _dispatch_email(cls, sender_func, *args):
        try:
            threading.Thread(target=sender_func, args=args, daemon=True).start()
        except Exception:
            logger.warning("Could not dispatch email thread", exc_info=True)

    @classmethod
    def _smtp_settings(cls):
        enabled = os.environ.get('ENABLE_EMAIL_SENDING', 'true').lower() in ('1', 'true', 'yes')
        if not enabled:
            logger.warning("Email sending disabled by ENABLE_EMAIL_SENDING. Skipping SMTP send.")
            return None

        server = os.environ.get('MAIL_SERVER')
        username = os.environ.get('MAIL_USERNAME')
        password = os.environ.get('MAIL_PASSWORD')
        if not all([server, username, password]):
            return None
        return {
            "server": server,
            "port": int(os.environ.get('MAIL_PORT', '587')),
            "username": username,
            "password": password,
            "sender": os.environ.get('MAIL_DEFAULT_SENDER', username),
            "use_tls": os.environ.get('MAIL_USE_TLS', 'true').lower() in ('1', 'true', 'yes'),
            "timeout": int(os.environ.get('SMTP_TIMEOUT_SECONDS', '8')),
        }

    @classmethod
    def _send_email(cls, recipient, subject, text_content, html_content):
        cfg = cls._smtp_settings()
        if not cfg:
            logger.warning("SMTP not configured or disabled. Skipping email to %s", recipient)
            return

        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = cfg['sender']
        message['To'] = recipient
        message.attach(MIMEText(text_content, 'plain'))
        message.attach(MIMEText(html_content, 'html'))

        try:
            with smtplib.SMTP(cfg['server'], cfg['port'], timeout=cfg['timeout']) as server:
                if cfg['use_tls']:
                    server.starttls()
                server.login(cfg['username'], cfg['password'])
                server.sendmail(cfg['sender'], recipient, message.as_string())
        except Exception as exc:
            logger.warning("Email send failed for %s: %s", recipient, exc)

    @classmethod
    def _build_reset_email_html(cls, username: str, reset_url: str) -> str:
        safe_username = html.escape(username or "", quote=True)
        safe_url = html.escape(reset_url or "", quote=True)
        return f"<p>Hello <strong>{safe_username}</strong>,</p><p><a href='{safe_url}'>Reset Password</a></p>"

    @classmethod
    def _build_welcome_email_html(cls, username: str) -> str:
        safe_username = html.escape(username or "", quote=True)
        return f"<p>Hi <strong>{safe_username}</strong>, welcome to Applyce!</p>"

    @classmethod
    def _send_reset_email(cls, email: str, username: str, token: str):
        try:
            reset_url = url_for('reset_password', token=token, _external=True)
        except RuntimeError:
            reset_url = f"{os.environ.get('BASE_URL', 'http://localhost:5000')}/reset-password/{token}"
        text = f"Hello {username},\n\nReset your password using this link: {reset_url}\nThis link expires in 1 hour."
        html_content = cls._build_reset_email_html(username, reset_url)
        cls._send_email(email, 'Applyce Password Reset', text, html_content)

    @classmethod
    def _send_welcome_email(cls, recipient_email: str, username: str):
        text = f"Hi {username}, welcome to Applyce!"
        html_content = cls._build_welcome_email_html(username)
        cls._send_email(recipient_email, 'Welcome to Applyce', text, html_content)

    @classmethod
    def reset_password(cls, token: str, new_password: str):
        valid, error = cls.validate_password(new_password)
        if not valid:
            return False, error
        user = User.get_by_reset_token(token)
        if not user or not user.verify_reset_token(token):
            return False, "Invalid or expired reset link."
        user.reset_password(new_password)
        return True, "Your password has been reset successfully. You can now log in."

    @classmethod
    def get_user_by_reset_token(cls, token: str):
        return User.get_by_reset_token(token)

    @classmethod
    def set_password_for_user(cls, user: User, password: str):
        valid, error = cls.validate_password(password)
        if not valid:
            return False, error
        user.set_password(password)
        db.session.commit()
        return True, "Password set successfully."

    @classmethod
    def link_oauth_account(cls, user: User, provider: str, provider_user_id: str, provider_email: str = None):
        provider_user_id = str(provider_user_id)
        existing = OAuthAccount.query.filter_by(provider=provider, provider_user_id=provider_user_id).first()
        if existing:
            if existing.user_id != user.id:
                raise OAuthLinkConflict("This OAuth account is already linked to another user.")
            return existing

        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_email=provider_email,
        )
        db.session.add(oauth_account)
        db.session.commit()
        return oauth_account

    @classmethod
    def _make_unique_username(cls, username_hint: str, provider: str = "oauth") -> str:
        base = cls.sanitize_oauth_username(username_hint, provider)
        candidate = base
        idx = 1
        while User.query.filter(func.lower(User.username) == candidate).first():
            idx += 1
            suffix = str(idx)
            candidate = f"{base[:80-len(suffix)]}{suffix}"
        return candidate

    @classmethod
    def get_or_create_oauth_user(cls, provider: str, provider_user_id: str, email: str, username_hint: str):
        provider_user_id = str(provider_user_id)
        linked = OAuthAccount.query.filter_by(provider=provider, provider_user_id=provider_user_id).first()
        if linked:
            return linked.user

        email_norm = cls.normalize_email(email)
        candidate_user = User.query.filter(func.lower(User.email) == email_norm).first() if email_norm else None

        if candidate_user:
            if candidate_user.password_hash:
                raise OAuthNeedsLinking("An account with this email already exists. Please log in and link GitHub.")
            cls.link_oauth_account(candidate_user, provider, provider_user_id, provider_email=email_norm)
            return candidate_user

        username_seed = username_hint or (email_norm.split('@')[0] if email_norm and '@' in email_norm else f'{provider}_user')
        original_seed = username_seed
        
        # Handle race condition in username generation by retrying with a random suffix
        max_retries = 5
        for attempt in range(max_retries):
            try:
                username = cls._make_unique_username(username_seed, provider)
                user = User(
                    username=username,
                    email=email_norm or f"{username}@users.noreply.github.com",
                    is_active=True,
                    password_hash=None,
                )
                db.session.add(user)
                db.session.commit()
                
                cls.link_oauth_account(user, provider, provider_user_id, provider_email=email_norm)
                return user
            except IntegrityError as exc:
                db.session.rollback()
                if attempt < max_retries - 1:
                    logger.warning("Username collision during OAuth user creation (attempt %s/%s), retrying...", attempt + 1, max_retries)
                    # Reset to original seed with a random suffix to avoid compounding
                    username_seed = f"{original_seed}_{random.randint(1000, 9999)}"
                else:
                    logger.error("Failed to create OAuth user after %s attempts due to IntegrityError: %s", max_retries, exc)
                    raise
