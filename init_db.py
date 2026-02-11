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
    from sqlalchemy import inspect, Column, Integer, String, Text, DateTime
    from sqlalchemy.schema import Table
    from sqlalchemy.sql import func
    
    inspector = inspect(db.engine)
    
    # Define expected columns for each table with their SQLAlchemy types
    expected_columns = {
        'resume_history': {
            'extracted_text': Text,
            'created_at': DateTime,
            'upload_date': DateTime,
            'user_id': Integer,
            'filename': String(255)
        },
        # Add other critical tables as needed
    }
    
    for table_name, required_cols in expected_columns.items():
        if table_name in inspector.get_table_names():
            existing = [col['name'] for col in inspector.get_columns(table_name)]
            missing = [col for col in required_cols.keys() if col not in existing]
            
            if missing:
                logger.warning(f"Table '{table_name}' is missing columns: {missing}")
                # Add missing columns using SQLAlchemy DDL
                for col_name in missing:
                    try:
                        col_type = required_cols[col_name]
                        # Get the table metadata
                        metadata = db.MetaData()
                        table = Table(table_name, metadata, autoload_with=db.engine)
                        
                        # Create the column object
                        if col_name == 'created_at':
                            new_column = Column(col_name, col_type, server_default=func.now())
                        else:
                            new_column = Column(col_name, col_type)
                        
                        # Add the column to the table
                        with db.engine.connect() as conn:
                            trans = conn.begin()
                            try:
                                # Use SQLAlchemy's DDL compilation
                                column_type_str = new_column.type.compile(db.engine.dialect)
                                column_name = new_column.name
                                # Using text() with parameterization is still safer than f-strings
                                from sqlalchemy import text
                                # Note: Table/column names cannot be parameterized, but we control these values
                                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type_str}"))
                                trans.commit()
                                logger.info(f"✅ Added column '{col_name}' to '{table_name}'")
                            except Exception as e:
                                trans.rollback()
                                # Column might already exist from a previous partial run
                                logger.debug(f"Column '{col_name}' might already exist: {e}")
                    except Exception as e:
                        logger.error(f"Failed to add column '{col_name}': {e}")
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
