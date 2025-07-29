#!/usr/bin/env python3
"""
Database Migration Script for Enhanced User Model
Run this on your production server to add new profile fields
"""

import mysql.connector
import os
from datetime import datetime

def get_db_connection():
    """Get database connection from environment or user input"""
    try:
        # Try to get from environment first
        connection = mysql.connector.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            user=os.getenv('DATABASE_USER', input("Database username: ")),
            password=os.getenv('DATABASE_PASSWORD', input("Database password: ")),
            database=os.getenv('DATABASE_NAME', input("Database name: "))
        )
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return None

def check_column_exists(cursor, table_name, column_name):
    """Check if a column already exists in the table"""
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name}' 
        AND COLUMN_NAME = '{column_name}'
        AND TABLE_SCHEMA = DATABASE()
    """)
    return cursor.fetchone()[0] > 0

def migrate_user_table():
    """Add new profile fields to user table"""
    print("🗄️  Starting User Table Migration...")
    print(f"📅 Migration Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Define the new columns to add
        new_columns = [
            ("first_name", "VARCHAR(100)"),
            ("last_name", "VARCHAR(100)"),
            ("phone", "VARCHAR(20)"),
            ("address", "TEXT"),
            ("city", "VARCHAR(100)"),
            ("state", "VARCHAR(100)"),
            ("postal_code", "VARCHAR(20)"),
            ("country", "VARCHAR(100)"),
            ("profile_completed", "BOOLEAN DEFAULT FALSE"),
            ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        print("🔍 Checking existing columns...")
        
        # Check which columns already exist
        existing_columns = []
        missing_columns = []
        
        for column_name, column_type in new_columns:
            if check_column_exists(cursor, 'user', column_name):
                existing_columns.append(column_name)
                print(f"  ✅ Column '{column_name}' already exists")
            else:
                missing_columns.append((column_name, column_type))
                print(f"  ➕ Column '{column_name}' needs to be added")
        
        if not missing_columns:
            print("\n🎉 All columns already exist! No migration needed.")
            return True
        
        print(f"\n📝 Adding {len(missing_columns)} new columns...")
        
        # Add missing columns
        for column_name, column_type in missing_columns:
            try:
                alter_sql = f"ALTER TABLE user ADD COLUMN {column_name} {column_type}"
                print(f"  Adding {column_name}...")
                cursor.execute(alter_sql)
                print(f"  ✅ Successfully added {column_name}")
            except mysql.connector.Error as e:
                print(f"  ❌ Failed to add {column_name}: {e}")
                return False
        
        # Commit all changes
        connection.commit()
        
        print("\n✅ Migration completed successfully!")
        print("📊 Migration Summary:")
        print(f"  • Existing columns: {len(existing_columns)}")
        print(f"  • Added columns: {len(missing_columns)}")
        print(f"  • Total profile fields: {len(new_columns)}")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Migration failed: {e}")
        connection.rollback()
        return False
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Database connection closed.")

def verify_migration():
    """Verify that all columns were added correctly"""
    print("\n🔍 Verifying migration...")
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Get all columns in user table
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'user' 
            AND TABLE_SCHEMA = DATABASE()
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        
        print("📋 Current User Table Structure:")
        print("-" * 60)
        for column_name, data_type, is_nullable, column_default in columns:
            nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
            default = f"DEFAULT {column_default}" if column_default else ""
            print(f"  {column_name:<20} {data_type:<15} {nullable:<10} {default}")
        
        print("-" * 60)
        print(f"✅ Total columns: {len(columns)}")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Verification failed: {e}")
        return False
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    """Main migration function"""
    print("🚀 Database Migration for Enhanced User Model")
    print("This script will add profile fields to your user table.")
    print("Make sure you have a backup of your database before proceeding!")
    print("=" * 60)
    
    # Ask for confirmation
    confirm = input("Do you want to proceed with the migration? (yes/no): ").lower()
    if confirm not in ['yes', 'y']:
        print("❌ Migration cancelled.")
        return
    
    # Run migration
    success = migrate_user_table()
    
    if success:
        verify_migration()
        print("\n🎉 Migration completed successfully!")
        print("Your denncathy.co.ke site now supports enhanced user profiles!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        print("Contact your hosting provider if you need assistance.")

if __name__ == "__main__":
    main()
