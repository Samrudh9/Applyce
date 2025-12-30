# Database Setup Instructions

This document provides instructions for setting up the database for the SkillFit Career Recommendation Application.

## Quick Start

The application supports two database configurations:
1. **SQLite** (Local Development) - No setup required
2. **PostgreSQL** (Production - Supabase or Render) - Requires configuration

## Local Development (SQLite)

For local development, the application automatically uses SQLite. No additional setup is required.

1. Install dependencies:
   ```bash
   pip install -r REQUIREMENTS.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The SQLite database will be automatically created at `instance/skillfit.db`.

## Production Setup (Supabase PostgreSQL)

### Prerequisites

- A Supabase account (free tier available at https://supabase.com)
- Python 3.8 or higher
- All dependencies installed (`pip install -r REQUIREMENTS.txt`)

### Step 1: Create Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Fill in project details:
   - Project name: `skillfit` (or your preferred name)
   - Database password: Choose a strong password
   - Region: Select closest to your users
4. Click "Create new project"
5. Wait for provisioning (1-2 minutes)

### Step 2: Set Up Database Schema

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Copy the entire contents of `supabase_schema.sql`
4. Paste into the editor and click "Run"
5. Verify tables in **Table Editor** section

### Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Get your connection string:
   - In Supabase: **Settings** → **Database** → **Connection string** → **URI**
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

3. Edit `.env` file:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=production
   ```

4. **Important**: Replace `[YOUR-PASSWORD]` with your actual database password

### Step 4: Run the Application

```bash
python app.py
```

Look for this confirmation:
```
📦 Using PostgreSQL (Supabase/Render)
✅ Database tables created/verified!
✅ Database ready!
```

## Deployment to Render (or other platforms)

### On Render:

1. Create a new Web Service
2. Connect your GitHub repository
3. Add environment variables in the Render dashboard:
   - `DATABASE_URL`: Your Supabase connection string
   - `SECRET_KEY`: A secure random string
   - `FLASK_ENV`: `production`
   - `ADMIN_ID`: Your admin email (optional)
   - `ADMIN_PASSWORD`: Your admin password (optional)

4. Deploy

### On Heroku:

```bash
heroku config:set DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres"
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set FLASK_ENV="production"
git push heroku main
```

## Database Schema

The application uses the following main tables:

### Users Table
Stores user account information and authentication data.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    -- Additional fields for password reset, freemium tracking, etc.
);
```

### Resume History Table
Tracks all resume uploads and analysis results.

```sql
CREATE TABLE resume_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(256) NOT NULL,
    upload_date TIMESTAMP DEFAULT NOW(),
    extracted_text TEXT,
    experience_level VARCHAR(50),
    target_role VARCHAR(50),
    overall_score FLOAT DEFAULT 0,
    ats_score FLOAT DEFAULT 0,
    -- Additional fields for scores, skills, career predictions, etc.
);
```

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | No | SQLite (local) |
| `SECRET_KEY` | Flask secret key for sessions | Yes (prod) | Random (dev) |
| `FLASK_ENV` | Environment mode | No | `development` |
| `ADMIN_ID` | Admin login ID for backups | No | `admin@skillfit.onrender.com` |
| `ADMIN_PASSWORD` | Admin password | No | `skillfit@admin` |
| `ROADMAP_SUPPORT` | Enable roadmap features | No | `true` |
| `ML_CLASSIFIER_ENABLED` | Enable ML classifier | No | `false` |

## Troubleshooting

### Connection Errors

**Problem**: `could not connect to server`
- Verify connection string is correct
- Ensure password doesn't contain special characters (URL encode if needed)
- Check Supabase project is running

**Problem**: `fe_sendauth: no password supplied`
- Connection string missing password
- Verify `[YOUR-PASSWORD]` is replaced with actual password

### Schema Errors

**Problem**: `relation "users" does not exist`
- Run the `supabase_schema.sql` script in Supabase SQL Editor
- Verify tables exist in Table Editor

**Problem**: `column "xyz" does not exist`
- Re-run the schema script
- Check for any migration errors

### Permission Errors

**Problem**: `permission denied for table users`
- Verify your database user has proper permissions
- Check Supabase project settings

## Migration from Render

If you're migrating from Render PostgreSQL to Supabase, see the detailed guide in [MIGRATION.md](MIGRATION.md).

## Backup and Recovery

### Manual Backup

Export data from Supabase:
```bash
pg_dump postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres > backup.sql
```

### Restore Backup

Import data to Supabase:
```bash
psql postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres < backup.sql
```

### Automated Backups

Supabase Pro plan includes automated daily backups. Free tier requires manual backups.

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` for a reason
2. **Use strong passwords** - Generate with password manager
3. **Rotate credentials** - Change passwords periodically
4. **Restrict access** - Use Supabase RLS policies if needed
5. **Monitor usage** - Check Supabase dashboard regularly

## Database Maintenance

### Check Connection

```python
from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("✅ Database connected!")
```

### View Table Info

In Supabase SQL Editor:
```sql
-- List all tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Count rows in a table
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM resume_history;
```

### Reset Database (⚠️ Deletes all data)

```sql
DROP TABLE IF EXISTS resume_history CASCADE;
DROP TABLE IF EXISTS users CASCADE;
-- Then re-run supabase_schema.sql
```

## Support

- **Application Issues**: Create an issue in the GitHub repository
- **Database Issues**: Check [MIGRATION.md](MIGRATION.md) troubleshooting section
- **Supabase Help**: https://supabase.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Last Updated**: December 2024
