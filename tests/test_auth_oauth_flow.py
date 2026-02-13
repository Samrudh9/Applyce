from services.auth_service import AuthService


def test_normalize_email():
    assert AuthService.normalize_email('  USER@Example.COM ') == 'user@example.com'


def test_validate_password_policy():
    ok, _ = AuthService.validate_password('longenough')
    bad, _ = AuthService.validate_password('short')
    assert ok is True
    assert bad is False
