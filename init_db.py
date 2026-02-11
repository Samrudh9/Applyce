#!/usr/bin/env python3
"""
Database initialization script for Applyce.
Creates all database tables if they don't exist and adds missing columns.
"""

import sys
import os
import logging

# Add current directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_add_missing_columns(app, db):
    """Check for missing columns and add them"""
    from sqlalchemy import inspect, text
    
    inspector = inspect(db.engine)
    
    # Define expected columns for each table with their types
    expected_columns = {
        'resume_history': {
            'extracted_text': 'TEXT',
            'created_at': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
            'upload_date': 'DATETIME',
            'user_id': 'INTEGER',
            'filename': 'VARCHAR(255)'
        },
        # Add other critical tables as needed
    }
    
    for table_name, required_cols in expected_columns.items():
        if table_name in inspector.get_table_names():
            existing = [col['name'] for col in inspector.get_columns(table_name)]
            missing = [col for col in required_cols.keys() if col not in existing]
            
            if missing:
                logger.warning(f"Table '{table_name}' is missing columns: {missing}")
                # Add missing columns
                for col in missing:
                    try:
                        col_type = required_cols[col]
                        with db.engine.connect() as conn:
                            # Start a transaction
                            trans = conn.begin()
                            try:
                                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col} {col_type}"))
                                trans.commit()
                                logger.info(f"✅ Added column '{col}' to '{table_name}'")
                            except Exception as e:
                                trans.rollback()
                                # Column might already exist, log and continue
                                logger.debug(f"Could not add column '{col}': {e}")
                    except Exception as e:
                        logger.error(f"Failed to add column '{col}': {e}")
            else:
                logger.info(f"✅ Table '{table_name}' has all required columns")

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
            
            # Check and add missing columns
            print("🔍 Checking for missing columns...")
            check_and_add_missing_columns(app, db)
            
            # Verify tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 Database has {len(tables)} table(s):")
                for table in sorted(tables):
                    columns = inspector.get_columns(table)
                    print(f"   - {table} ({len(columns)} columns)")
            else:
                print("⚠️  Warning: No tables found in database")
            
            print("✅ Database initialized and columns verified!")
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
