#!/usr/bin/env python3
"""
Sync Products from Production Database
========================================
This script exports product data from your production database
and imports it into your local development database.

Usage:
    python3 sync_products_from_production.py
"""

import pymysql
import json
import sys
from getpass import getpass

# Production database credentials
PROD_HOST = "localhost"  # Or your Host Africa server IP if accessing remotely
PROD_USER = "denncath_flaskapp"
PROD_PASSWORD = "z4jfLsJZHPSJQLzE5q2c"
PROD_DB = "denncath_flaskapp"

# Local database credentials (from your .env)
LOCAL_HOST = "localhost"
LOCAL_USER = "root"
LOCAL_PASSWORD = "Root2026"
LOCAL_DB = "grocery_db"


def export_from_production():
    """Export categories and products from production database"""
    print("🔄 Connecting to production database...")
    
    try:
        # Connect to production database
        prod_conn = pymysql.connect(
            host=PROD_HOST,
            user=PROD_USER,
            password=PROD_PASSWORD,
            database=PROD_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected to production database!")
        
        with prod_conn.cursor() as cursor:
            # Export categories
            print("\n📦 Exporting categories...")
            cursor.execute("SELECT * FROM category ORDER BY id")
            categories = cursor.fetchall()
            print(f"✅ Found {len(categories)} categories")
            
            # Export products
            print("\n📦 Exporting products...")
            cursor.execute("SELECT * FROM product ORDER BY id")
            products = cursor.fetchall()
            print(f"✅ Found {len(products)} products")
            
        prod_conn.close()
        
        return categories, products
        
    except pymysql.Error as e:
        print(f"❌ Error connecting to production database: {e}")
        print("\n💡 If you can't access production remotely, use Option 2 below.")
        return None, None


def import_to_local(categories, products):
    """Import categories and products to local database"""
    print("\n🔄 Connecting to local database...")
    
    try:
        # Connect to local database
        local_conn = pymysql.connect(
            host=LOCAL_HOST,
            user=LOCAL_USER,
            password=LOCAL_PASSWORD,
            database=LOCAL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected to local database!")
        
        with local_conn.cursor() as cursor:
            # Import categories first (due to foreign key constraint)
            print("\n📥 Importing categories...")
            category_count = 0
            for cat in categories:
                try:
                    cursor.execute(
                        "INSERT INTO category (id, name) VALUES (%s, %s) "
                        "ON DUPLICATE KEY UPDATE name = VALUES(name)",
                        (cat['id'], cat['name'])
                    )
                    category_count += 1
                except pymysql.Error as e:
                    print(f"⚠️  Warning importing category {cat['name']}: {e}")
            
            local_conn.commit()
            print(f"✅ Imported {category_count} categories")
            
            # Import products
            print("\n📥 Importing products...")
            product_count = 0
            for prod in products:
                try:
                    cursor.execute(
                        """
                        INSERT INTO product (id, name, description, price, stock, image_url, category_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            name = VALUES(name),
                            description = VALUES(description),
                            price = VALUES(price),
                            stock = VALUES(stock),
                            image_url = VALUES(image_url),
                            category_id = VALUES(category_id)
                        """,
                        (
                            prod['id'],
                            prod['name'],
                            prod.get('description'),
                            prod['price'],
                            prod['stock'],
                            prod.get('image_url'),
                            prod['category_id']
                        )
                    )
                    product_count += 1
                except pymysql.Error as e:
                    print(f"⚠️  Warning importing product {prod['name']}: {e}")
            
            local_conn.commit()
            print(f"✅ Imported {product_count} products")
            
        local_conn.close()
        
        print("\n🎉 SUCCESS! Product data synced from production to local database!")
        print(f"   Categories: {category_count}")
        print(f"   Products: {product_count}")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Error connecting to local database: {e}")
        return False


def save_to_json_file(categories, products):
    """Save data to JSON file for manual import"""
    data = {
        'categories': categories,
        'products': products
    }
    
    filename = 'production_data_export.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"\n💾 Data saved to: {filename}")
    print(f"   You can import this later using: python3 import_from_json.py")


def main():
    print("=" * 60)
    print("🚀 Production to Local Database Sync")
    print("=" * 60)
    
    print("\n⚠️  NOTE: This will connect to production database to export data.")
    print("   If you can't access production remotely, see Option 2 below.\n")
    
    # Export from production
    categories, products = export_from_production()
    
    if not categories or not products:
        print("\n" + "=" * 60)
        print("📋 OPTION 2: Manual Export from Production Server")
        print("=" * 60)
        print("\nRun this command on your Host Africa server:")
        print("\n  ssh denncath@da11.host-africa.com")
        print("  cd ~/public_html")
        print("  mysqldump -u denncath_flaskapp -p denncath_flaskapp category product > products_export.sql")
        print("\nThen download the file and import locally:")
        print("  mysql -u root -p grocery_db < products_export.sql")
        print("=" * 60)
        return
    
    # Save to JSON as backup
    save_to_json_file(categories, products)
    
    # Import to local
    import_to_local(categories, products)


if __name__ == "__main__":
    main()
