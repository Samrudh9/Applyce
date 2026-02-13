import re

import pytest

from app import app
from models import db
from models.oauth_account import OAuthAccount
from models.user import User
from services.auth_service import AuthService, OAuthLinkConflict, OAuthNeedsLinking


@pytest.fixture(autouse=True)
def setup_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()


def test_linking_conflict_raises_for_different_user():
    with app.app_context():
        user1 = User(username='u1', email='u1@example.com', password_hash='x')
        user2 = User(username='u2', email='u2@example.com', password_hash='x')
        db.session.add_all([user1, user2])
        db.session.commit()

        AuthService.link_oauth_account(user1, 'github', 'gid-123', provider_email='u1@example.com')
        with pytest.raises(OAuthLinkConflict):
            AuthService.link_oauth_account(user2, 'github', 'gid-123', provider_email='u2@example.com')


def test_get_or_create_oauth_user_no_email_takeover_for_password_users():
    with app.app_context():
        user = User(username='localuser', email='same@example.com', password_hash='has_local_password')
        db.session.add(user)
        db.session.commit()

        with pytest.raises(OAuthNeedsLinking):
            AuthService.get_or_create_oauth_user('github', 'new-gid', 'same@example.com', 'gh-name')


def test_github_username_is_sanitized_to_local_rules():
    with app.app_context():
        user = AuthService.get_or_create_oauth_user(
            provider='github',
            provider_user_id='gh-42',
            email='gh42@example.com',
            username_hint='Bad.User-Name!!',
        )
        assert re.match(r'^[a-z0-9_]{3,80}$', user.username)


def test_email_html_escaping_for_username_and_url():
    malicious = '<script>alert(1)</script>'
    html_welcome = AuthService._build_welcome_email_html(malicious)
    assert '<script>' not in html_welcome
    assert '&lt;script&gt;alert(1)&lt;/script&gt;' in html_welcome

    html_reset = AuthService._build_reset_email_html(malicious, "https://example.com/reset?q='bad'")
    assert '<script>' not in html_reset
    assert '&#x27;bad&#x27;' in html_reset


def test_callback_handles_github_emails_failure_gracefully(monkeypatch):
    class FakeResp:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

    class FakeOAuth:
        def authorize_access_token(self):
            return {'access_token': 'token'}

        def get(self, endpoint):
            if endpoint == 'user':
                return FakeResp({'id': 12345, 'login': 'ghlogin', 'email': None})
            if endpoint == 'user/emails':
                raise RuntimeError('email endpoint down')
            raise AssertionError('unexpected endpoint')

    monkeypatch.setattr('app.github_oauth', FakeOAuth())

    client = app.test_client()
    with client.session_transaction() as sess:
        sess['github_oauth_state'] = 'state-1'

    resp = client.get('/auth/github/callback?state=state-1', follow_redirects=False)
    assert resp.status_code in (302, 303)

    with app.app_context():
        user = User.query.filter_by(username='ghlogin').first()
        assert user is not None
        oa = OAuthAccount.query.filter_by(provider='github', provider_user_id='12345').first()
        assert oa is not None
