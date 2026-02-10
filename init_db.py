#!/usr/bin/env python3
"""
Database initialization script for Applyce.
Creates all database tables if they don't exist.
"""

import sys
import os

# Add current directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database tables."""
    try:
        print("🔧 Initializing database...")
        
        # Import app and db after path is set
        from app import app, db
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 Created {len(tables)} table(s):")
                for table in sorted(tables):
                    print(f"   - {table}")
            else:
                print("⚠️  Warning: No tables were created")
                
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
