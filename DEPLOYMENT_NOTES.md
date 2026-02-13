# Deployment Notes (Render)

## 1) Environment variables (Render Dashboard → Service → Environment)
Set the following (no secrets in git):

- `SECRET_KEY` (strong random)
- `DATABASE_URL` (Render Postgres external URL)
- `DB_SSLMODE=require`
- `SQLALCHEMY_POOL_RECYCLE=300`
- `SQLALCHEMY_POOL_SIZE=5`
- `SQLALCHEMY_MAX_OVERFLOW=5`
- `BASE_URL=https://your-domain.com`

### OAuth
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `OAUTH_REDIRECT_URL=https://your-domain.com/auth/github/callback`

### SMTP (optional but recommended)
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS=true`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`
- `SMTP_TIMEOUT_SECONDS=8`

> If SMTP is missing/misconfigured, registration and reset flows continue without blocking.

## 2) Run migrations

If this is the first migration setup in your environment:

```bash
flask db init
```

Create migration (for future schema changes):

```bash
flask db migrate -m "schema updates"
```

Apply migrations:

```bash
flask db upgrade
```

For this repository, a migration file is already included under:
- `migrations/versions/20260212_01_auth_and_resume_schema.py`

On Render Shell:

```bash
python -m flask db upgrade
```

## 3) Health endpoints

- `GET /health` → always fast liveness (does not call DB)
- `GET /ready` → readiness details including DB status (returns 200 with status payload)

## 4) Startup behavior

No automatic `db.create_all()`/auto-migration at import time. Use `flask db upgrade` during deploy.
