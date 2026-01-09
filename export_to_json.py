#!/usr/bin/env python3
"""
Export Products from Production Database to JSON
Run this on Host Africa server: python3 export_to_json.py
"""

import pymysql
import json

# Production database credentials
DB_HOST = "localhost"
DB_USER = "denncath_flaskapp"
DB_PASSWORD = "z4jfLsJZHPSJQLzE5q2c"
DB_NAME = "denncath_flaskapp"

print("🔄 Connecting to database...")

try:
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print("✅ Connected!")
    
    with conn.cursor() as cursor:
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
        
    conn.close()
    
    # Save to JSON
    data = {
        'categories': categories,
        'products': products
    }
    
    filename = 'products_export.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"\n💾 Data exported to: {filename}")
    print(f"\n📥 Download this file to your local machine and run:")
    print(f"   python3 import_from_json.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
