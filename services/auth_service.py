"""
Authentication service for user management.
"""

import re
import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models import db
from models.user import User
from flask import url_for
from flask_login import login_user, logout_user
from models import db
from models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling user authentication."""
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username format."""
        if not username or len(username) < 3 or len(username) > 80:
            return False, "Username must be between 3 and 80 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength."""
        if not password or len(password) < AuthService.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {AuthService.MIN_PASSWORD_LENGTH} characters"
        return True, None
    
    @classmethod
    def register_user(cls, username, email, password):
        """
        Register a new user.
        
        Returns:
            tuple: (success: bool, user_or_error: User or str)
        """
        try:
            # Validate input
            valid, error = cls.validate_username(username)
            if not valid:
                return False, error

            if not cls.validate_email(email):
                return False, "Invalid email format"

            valid, error = cls.validate_password(password)
            if not valid:
                return False, error

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return False, "Username already taken"

            if User.query.filter_by(email=email).first():
                return False, "Email already registered"

            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            try:
                cls._send_welcome_email(user.email, user.username)
            except Exception:
                logger.exception("Welcome email failed after registration")
            return True, user
        except Exception as e:
            db.session.rollback()
            logger.exception("Registration failed")
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def authenticate_user(username_or_email, password):
        """
        Authenticate a user by username/email and password.
        
        Returns:
            tuple: (success: bool, user_or_error: User or str)
        """
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email)
        ).first()
        
        if not user:
            return False, "Invalid username/email or password"
        
        if not user.is_active:
            return False, "Account is disabled"
        
        if not user.check_password(password):
            return False, "Invalid username/email or password"
        
        return True, user
    
    @staticmethod
    def login(user, remember=False):
        """
        Log in a user using Flask-Login.
        
        Args:
            user: User object
            remember: Whether to remember the user
            
        Returns:
            bool: Success status
        """
        try:
            login_user(user, remember=remember)
            user.update_last_login()
            return True
        except Exception:
            return False
    
    @staticmethod
    def logout():
        """Log out the current user."""
        logout_user()
        return True
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID (for Flask-Login loader)."""
        return User.query.get(int(user_id))
    
    # ===== Forgot Password Methods =====
    
    @classmethod
    def initiate_password_reset(cls, email: str) -> tuple:
        """
        Initiate password reset process by generating token and sending email.
        
        Args:
            email: User's email address
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Don't reveal if email exists for security
            return True, "If this email is registered, you will receive a password reset link."
        
        if not user.is_active:
            return True, "If this email is registered, you will receive a password reset link."
        
        # Generate reset token
        token = user.generate_reset_token()
        
        # Send reset email
        try:
            cls._send_reset_email(user.email, user.username, token)
            logger.info(f"Password reset email sent to {email}")
            return True, "If this email is registered, you will receive a password reset link."
        except Exception as e:
            logger.error(f"Failed to send password reset email: {e}")
            # Clear the token since email failed
            user.clear_reset_token()
            return False, "Failed to send reset email. Please try again later."
    
    @classmethod
    def _send_reset_email(cls, email: str, username: str, token: str):
        """
        Send password reset email using Gmail SMTP.
        
        Args:
            email: Recipient email address
            username: User's username for personalization
            token: The reset token
        """
        # Get email credentials from environment
        sender_email = os.environ.get('EMAIL_ADDRESS')
        sender_password = os.environ.get('EMAIL_PASSWORD')
        
        if not sender_email or not sender_password:
            logger.warning("Email credentials not configured. Skipping email send.")
            # In development, log that a reset was requested (without exposing the token)
            logger.info(f"Development mode - Password reset requested for user")
            return
        
        # Build reset URL
        try:
            reset_url = url_for('reset_password', token=token, _external=True)
        except RuntimeError:
            # If outside request context, build URL manually
            base_url = os.environ.get('BASE_URL', 'http://localhost:5000')
            reset_url = f"{base_url}/reset-password/{token}"
        
        # Create email message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Account - Password Reset Request'
        message['From'] = sender_email
        message['To'] = email
        
        # Plain text version
        text_content = f"""
Hello {username},

You requested a password reset for your Applyce account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this reset, you can safely ignore this email.

Best regards,
The Applyce Team
        """
        
        # HTML version
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Inter', Arial, sans-serif; background-color: #0a0b0f; color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #1a1b22; border-radius: 16px; padding: 40px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .logo {{ font-size: 28px; font-weight: 700; background: linear-gradient(135deg, #00c2ff, #00ffe0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .content {{ line-height: 1.6; }}
        .button {{ display: inline-block; background: linear-gradient(90deg, #00c2ff, #00ffe0); color: #000; padding: 14px 32px; border-radius: 12px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
        .footer {{ margin-top: 30px; font-size: 14px; color: #888; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀 Applyce</div>
        </div>
        <div class="content">
            <p>Hello <strong>{username}</strong>,</p>
            <p>You requested a password reset for your Applyce account.</p>
            <p>Click the button below to reset your password:</p>
            <p style="text-align: center;">
                <a href="{reset_url}" class="button">Reset Password</a>
            </p>
            <p style="font-size: 14px; color: #888;">
                This link will expire in 1 hour. If you didn't request this reset, you can safely ignore this email.
            </p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The Applyce Team</p>
        </div>
    </div>
</body>
        </html>
        """

        # Attach both versions
        message.attach(MIMEText(text_content, 'plain'))
        message.attach(MIMEText(html_content, 'html'))

        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())

    @classmethod
    def _send_welcome_email(cls, recipient_email: str, username: str) -> None:
        """
        Send a welcome email after successful registration.

        Args:
            recipient_email: Recipient email address
            username: User's username for personalization
        """
        try:
            smtp_server = os.environ.get('MAIL_SERVER', 'smtp-relay.brevo.com')
            smtp_port = int(os.environ.get('MAIL_PORT', 587))
            smtp_user = os.environ.get('MAIL_USERNAME')
            smtp_password = os.environ.get('MAIL_PASSWORD')
            sender = os.environ.get('MAIL_DEFAULT_SENDER', smtp_user or '')

            if not smtp_user or not smtp_password:
                logger.warning("SMTP credentials missing; welcome email not sent.")
                return

            message = MIMEMultipart('alternative')
            message['Subject'] = 'Welcome to Applyce'
            message['From'] = sender
            message['To'] = recipient_email

            text_body = f"""\
Hi {username},

Welcome to Applyce!

Your account has been successfully created.
Start analyzing your resume and exploring career paths.

– Applyce Team
"""
            html_body = f"""\
<!DOCTYPE html>
<html>
<body>
  <p>Hi <strong>{username}</strong>,</p>
  <p>Welcome to Applyce 🎯</p>
  <p>Your account has been successfully created.<br>
     Start analyzing your resume and exploring career paths.</p>
  <p>– Applyce Team</p>
</body>
</html>
"""
            message.attach(MIMEText(text_body, 'plain'))
            message.attach(MIMEText(html_body, 'html'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender, recipient_email, message.as_string())

            logger.info("Welcome email sent to %s", recipient_email)
        except Exception:
            logger.exception("Failed to send welcome email")
    
    @classmethod
    def reset_password(cls, token: str, new_password: str) -> tuple:
        """
        Reset user's password using the reset token.
        
        Args:
            token: The reset token
            new_password: The new password to set
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate new password
        valid, error = cls.validate_password(new_password)
        if not valid:
            return False, error
        
        # Find user with this token
        user = User.query.filter_by(reset_token=token).first()
        
        if not user:
            return False, "Invalid or expired reset link."
        
        if not user.verify_reset_token(token):
            return False, "This reset link has expired. Please request a new one."
        
        # Reset the password
        user.reset_password(new_password)
        logger.info(f"Password reset successful for user {user.username}")
        
        return True, "Your password has been reset successfully. You can now log in."
    
    @classmethod
    def get_user_by_reset_token(cls, token: str):
        """
        Get user by reset token for verification.
        
        Args:
            token: The reset token
            
        Returns:
            User or None
        """
        return User.query.filter_by(reset_token=token).first()
     
