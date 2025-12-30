# Database Migration Guide: Render PostgreSQL to Supabase

This guide walks you through migrating the SkillFit application database from Render PostgreSQL to Supabase PostgreSQL.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Supabase Setup](#supabase-setup)
3. [Schema Creation](#schema-creation)
4. [Application Configuration](#application-configuration)
5. [Testing the Connection](#testing-the-connection)
6. [Data Migration (Optional)](#data-migration-optional)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting the migration, ensure you have:
- A Supabase account (sign up at https://supabase.com)
- Access to your current Render PostgreSQL database (if you need to migrate existing data)
- Python 3.8+ installed locally
- PostgreSQL client tools (optional, for data migration)

## Supabase Setup

### Step 1: Create a New Supabase Project

1. Log in to your Supabase account at https://supabase.com
2. Click "New Project"
3. Fill in the project details:
   - **Name**: SkillFit (or your preferred name)
   - **Database Password**: Choose a strong password (save it securely!)
   - **Region**: Choose the region closest to your users
4. Click "Create new project"
5. Wait for the project to be provisioned (usually takes 1-2 minutes)

### Step 2: Get Your Database Connection String

1. In your Supabase project dashboard, go to **Settings** → **Database**
2. Under "Connection string", select the **URI** tab
3. Copy the connection string. It will look like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.etlpqbraqfxhstpnomms.supabase.co:5432/postgres
   ```
4. Replace `[YOUR-PASSWORD]` with the database password you created in Step 1

## Schema Creation

### Step 1: Run the SQL Schema Script

1. In your Supabase project dashboard, go to the **SQL Editor**
2. Click "New query"
3. Copy the contents of `supabase_schema.sql` from this repository
4. Paste it into the SQL editor
5. Click "Run" to execute the schema creation

This will create all necessary tables:
- `users` - User accounts and authentication
- `resume_history` - Resume upload history and analysis results
- `feedbacks` - User feedback collection
- `resumes` - Detailed resume storage
- `skill_patterns` - Learning patterns for AI improvement
- `user_preferences` - User settings and preferences
- `resume_versions` - Version tracking
- `job_patterns` - Job market patterns

### Step 2: Verify Tables Were Created

1. In Supabase, go to **Table Editor**
2. You should see all the tables listed in the left sidebar
3. Click on each table to verify the schema matches your requirements

## Application Configuration

### Step 1: Set Up Environment Variables

1. Copy the `.env.example` file to create your own `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Supabase connection string:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.etlpqbraqfxhstpnomms.supabase.co:5432/postgres
   
   # Flask Configuration
   FLASK_APP=app.py
   FLASK_ENV=production
   SECRET_KEY=your-super-secret-key-here
   
   # Optional: Admin credentials
   ADMIN_ID=admin@yourapp.com
   ADMIN_PASSWORD=your-secure-admin-password
   ```

3. **Important Security Notes**:
   - Never commit the `.env` file to version control
   - Use strong, unique passwords
   - Keep your database credentials secure
   - Regenerate `SECRET_KEY` for production

### Step 2: Install Dependencies

Make sure you have all required dependencies:

```bash
pip install -r REQUIREMENTS.txt
```

Key dependencies for PostgreSQL:
- `psycopg2-binary` - PostgreSQL adapter for Python
- `Flask-SQLAlchemy` - SQL ORM
- `Flask-Migrate` - Database migrations

### Step 3: Deploy to Production (Render/Other)

If deploying to Render or another platform:

1. Add the `DATABASE_URL` environment variable in your platform's settings:
   - **Render**: Dashboard → Environment → Add Environment Variable
   - Name: `DATABASE_URL`
   - Value: Your Supabase connection string

2. Add other required environment variables:
   - `SECRET_KEY`
   - `FLASK_ENV=production`
   - Any other custom configurations

3. Deploy your application

## Testing the Connection

### Local Testing

1. Ensure your `.env` file is configured with the Supabase connection string
2. Run the application locally:
   ```bash
   python app.py
   ```
3. Check the console output for:
   ```
   📦 Using PostgreSQL (Supabase/Render)
   ✅ Database tables created/verified!
   ✅ Database ready!
   ```

### Test Database Operations

1. **Register a new user**:
   - Navigate to `/register`
   - Create a test account
   - Verify the user appears in Supabase Table Editor

2. **Upload a resume**:
   - Login with your test account
   - Navigate to `/upload`
   - Upload a test resume
   - Check the `resume_history` table in Supabase

3. **View dashboard**:
   - Navigate to `/dashboard`
   - Verify your resume history is displayed correctly

## Data Migration (Optional)

If you have existing data in Render PostgreSQL that needs to be migrated:

### Option 1: Using pg_dump and psql

1. **Export data from Render**:
   ```bash
   pg_dump -h [RENDER_HOST] -U [RENDER_USER] -d [RENDER_DB] \
     --data-only --inserts -f render_data.sql
   ```

2. **Import data to Supabase**:
   ```bash
   psql postgresql://postgres:[PASSWORD]@db.etlpqbraqfxhstpnomms.supabase.co:5432/postgres \
     -f render_data.sql
   ```

### Option 2: Using Python Script

Create a migration script (`migrate_data.py`):

```python
import os
from sqlalchemy import create_engine
import pandas as pd

# Source (Render) database
source_url = os.getenv('RENDER_DATABASE_URL')
source_engine = create_engine(source_url)

# Destination (Supabase) database
dest_url = os.getenv('DATABASE_URL')
dest_engine = create_engine(dest_url)

# Tables to migrate
tables = ['users', 'resume_history', 'feedbacks', 'resumes']

for table in tables:
    print(f"Migrating {table}...")
    df = pd.read_sql_table(table, source_engine)
    df.to_sql(table, dest_engine, if_exists='append', index=False)
    print(f"✅ Migrated {len(df)} rows from {table}")
```

Run the script:
```bash
python migrate_data.py
```

### Option 3: Manual Migration (Small Datasets)

For small amounts of data:
1. Export data from Render as CSV in Supabase SQL Editor
2. Import CSV files into Supabase using the Table Editor UI

## Troubleshooting

### Connection Errors

**Error**: `could not connect to server`
- Verify your connection string is correct
- Check that your IP is not blocked (Supabase allows all IPs by default)
- Ensure the password doesn't contain special characters that need URL encoding

**Error**: `SSL connection required`
- Supabase requires SSL. The connection string should include `?sslmode=require`
- Add to your connection string if missing:
  ```
  postgresql://postgres:password@host:5432/postgres?sslmode=require
  ```

### Schema Errors

**Error**: `relation "users" already exists`
- The tables already exist. You can either:
  - Drop existing tables (⚠️ this deletes all data)
  - Skip table creation if they match your needs
  - Use `CREATE TABLE IF NOT EXISTS` (already in the provided schema)

**Error**: `column "xyz" does not exist`
- The application expects columns that aren't in your database
- Re-run the `supabase_schema.sql` script
- Or manually add missing columns using:
  ```sql
  ALTER TABLE table_name ADD COLUMN column_name TYPE;
  ```

### Application Errors

**Error**: `No module named 'psycopg2'`
- Install the PostgreSQL adapter:
  ```bash
  pip install psycopg2-binary
  ```

**Error**: `SQLALCHEMY_DATABASE_URI not set`
- Ensure `DATABASE_URL` is set in your environment variables
- Check your `.env` file is in the project root
- Verify `python-dotenv` is installed

### Performance Issues

If queries are slow:
1. Check indexes are created (they're in the schema)
2. Monitor your query performance in Supabase Dashboard → Database → Query Performance
3. Consider upgrading your Supabase plan for better performance

## Verification Checklist

Before going live, verify:

- [ ] All tables created successfully in Supabase
- [ ] Environment variables configured correctly
- [ ] User registration works
- [ ] User login works
- [ ] Resume upload and analysis works
- [ ] Dashboard displays correctly
- [ ] No console errors about database connections
- [ ] Data from Render (if applicable) migrated successfully
- [ ] Backup strategy in place

## Rollback Plan

If you need to rollback to Render:

1. Keep your Render database active during the migration period
2. Change the `DATABASE_URL` back to your Render connection string
3. Redeploy your application

## Support

- **Supabase Documentation**: https://supabase.com/docs
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/

## Next Steps

After successful migration:

1. **Monitor Performance**: Use Supabase's built-in monitoring tools
2. **Set Up Backups**: Configure automated backups in Supabase
3. **Security Audit**: Review Row Level Security (RLS) policies if needed
4. **Optimize Queries**: Use Supabase's query performance tools
5. **Scale as Needed**: Upgrade your Supabase plan based on usage

---

**Migration Date**: _[Add date when you migrate]_  
**Migrated By**: _[Add your name/team]_  
**Status**: _[Pending/In Progress/Complete]_
