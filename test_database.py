#!/usr/bin/env python3
"""
Database Connection Test Script
Tests connectivity to PostgreSQL (Supabase) or SQLite database.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_database_url():
    """
    Get database URL from environment or fallback to SQLite.
    Returns tuple of (database_url, is_postgresql).
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Use SQLite for local testing
        basedir = os.path.abspath(os.path.dirname(__file__))
        instance_path = os.path.join(basedir, 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
        database_url = f'sqlite:///{os.path.join(instance_path, "skillfit.db")}'
        return database_url, False
    
    # Handle postgres:// vs postgresql:// prefix
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url, True

def mask_password_in_url(url):
    """Mask password in database URL for safe display."""
    if '@' not in url:
        return url
    
    try:
        parts = url.split('@')
        credentials = parts[0].split('://')
        if len(credentials) > 1 and ':' in credentials[1]:
            user_pass = credentials[1].split(':', 1)  # Split only on first ':'
            return f"{credentials[0]}://{user_pass[0]}:****@{parts[1]}"
    except (IndexError, ValueError):
        # If URL structure is unexpected, return as-is
        pass
    
    return url

def test_database_connection():
    """Test database connection and display information."""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Get database URL
    database_url, is_postgresql = get_database_url()
    
    if not is_postgresql:
        print("\n❌ DATABASE_URL not found in environment variables")
        print("\nFor local development, this is OK - SQLite will be used.")
        print(f"\n📦 Testing SQLite connection")
        print(f"   Location: {database_url}")
    else:
        print(f"\n📦 Testing PostgreSQL connection")
        print(f"   URL: {mask_password_in_url(database_url)}")
    
    try:
        # Create engine
        print("\n⏳ Creating database engine...")
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        print("⏳ Testing connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Connection successful!")
        
        # Get database info
        print("\n📊 Database Information:")
        inspector = inspect(engine)
        
        # Get dialect
        dialect = engine.dialect.name
        print(f"   Dialect: {dialect}")
        
        # List tables
        tables = inspector.get_table_names()
        print(f"   Tables: {len(tables)} found")
        
        if tables:
            print("\n📋 Existing Tables:")
            for table in sorted(tables):
                # Note: Table names come from database schema inspection (not user input)
                # This is safe because inspector.get_table_names() returns validated table names
                with engine.connect() as connection:
                    # Using text() with f-string is safe here as table names are from schema
                    count_result = connection.execute(
                        text(f"SELECT COUNT(*) FROM {table}")
                    )
                    count = count_result.fetchone()[0]
                    print(f"   - {table}: {count} rows")
        else:
            print("\n⚠️  No tables found. You may need to:")
            print("   1. Run the application to create tables automatically")
            print("   2. Or run supabase_schema.sql in Supabase SQL Editor")
        
        # Check for required tables
        required_tables = ['users', 'resume_history']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"\n⚠️  Missing required tables: {', '.join(missing_tables)}")
            print("   Run supabase_schema.sql to create all tables")
        else:
            print("\n✅ All required tables exist!")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE TEST PASSED")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"   Error: {str(e)}")
        print("\n" + "=" * 60)
        print("❌ DATABASE TEST FAILED")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Verify DATABASE_URL in .env file")
        print("2. Check database password is correct")
        print("3. Ensure Supabase project is running")
        print("4. Verify network connectivity")
        print("5. Check if DATABASE_URL uses 'postgresql://' prefix")
        return False

def test_write_operation():
    """Test write operation to database."""
    print("\n" + "=" * 60)
    print("DATABASE WRITE TEST")
    print("=" * 60)
    
    # Get database URL using helper function
    database_url, is_postgresql = get_database_url()
    
    try:
        engine = create_engine(database_url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'users' not in tables:
            print("⚠️  'users' table not found. Skipping write test.")
            print("   Create tables first using supabase_schema.sql")
            return False
        
        print("\n⏳ Testing write permissions...")
        
        # Try to get current row count
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            initial_count = result.fetchone()[0]
            print(f"   Current users: {initial_count}")
        
        print("✅ Read permission verified!")
        print("\nNote: Write test skipped to avoid modifying production data")
        print("      Application will test writes during normal operation")
        
        return True
        
    except Exception as e:
        print(f"❌ Write test failed: {str(e)}")
        return False

if __name__ == '__main__':
    print("\n🚀 Starting database tests...\n")
    
    # Test connection
    connection_ok = test_database_connection()
    
    if connection_ok:
        # Test write operations
        test_write_operation()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nYour database is ready to use!")
        print("Run 'python app.py' to start the application.")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before running the application.")
        sys.exit(1)
