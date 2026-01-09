#!/usr/bin/env python3
"""
Import Products from JSON file to Local Database
Usage: python3 import_from_json.py [json_file]
"""

import pymysql
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Local database credentials
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_USER = os.getenv("DATABASE_USER", "root")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME", "grocery_db")

def import_from_json(json_file):
    """Import categories and products from JSON file"""
    
    # Check if file exists
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return False
    
    # Load JSON data
    print(f"📂 Loading data from {json_file}...")
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    categories = data.get('categories', [])
    products = data.get('products', [])
    
    print(f"✅ Loaded {len(categories)} categories and {len(products)} products")
    
    # Connect to local database
    print("\n🔄 Connecting to local database...")
    
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("✅ Connected to local database!")
        
        with conn.cursor() as cursor:
            # Import categories first
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
                    print(f"  ✓ {cat['name']}")
                except pymysql.Error as e:
                    print(f"  ⚠️  Warning: {cat['name']}: {e}")
            
            conn.commit()
            print(f"\n✅ Imported {category_count}/{len(categories)} categories")
            
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
                    if product_count % 10 == 0:
                        print(f"  ✓ Imported {product_count} products...")
                except pymysql.Error as e:
                    print(f"  ⚠️  Warning: {prod['name']}: {e}")
            
            conn.commit()
            print(f"\n✅ Imported {product_count}/{len(products)} products")
            
        conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Product data imported to local database!")
        print("=" * 60)
        print(f"   Categories: {category_count}")
        print(f"   Products: {product_count}")
        print("\n🚀 You can now run: python3 app.py")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("=" * 60)
    print("📥 Import Products from JSON to Local Database")
    print("=" * 60)
    print()
    
    # Get JSON file from command line or use default
    json_file = sys.argv[1] if len(sys.argv) > 1 else "products_export.json"
    
    import_from_json(json_file)


if __name__ == "__main__":
    main()
