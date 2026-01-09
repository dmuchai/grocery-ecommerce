# Syncing Products from Production to Local Development

## Quick Guide

There are two methods to sync product data from production to your local database:

---

## Method 1: SSH Access (Recommended) 

### Step 1: Export from Production Server

SSH into your Host Africa server and run:

```bash
ssh denncath@da11.host-africa.com
cd ~/public_html
python3 export_to_json.py
```

This will create `products_export.json` with all your categories and products.

### Step 2: Download to Local Machine

From your local machine:

```bash
scp denncath@da11.host-africa.com:~/public_html/products_export.json ~/grocery-ecommerce/
```

### Step 3: Import to Local Database

```bash
cd ~/grocery-ecommerce
source venv/bin/activate
python3 import_from_json.py
```

Done! 🎉

---

## Method 2: MySQL Dump (Alternative)

### Step 1: Export SQL on Production Server

```bash
ssh denncath@da11.host-africa.com
cd ~/public_html
mysqldump -u denncath_flaskapp -p denncath_flaskapp category product > products.sql
```

Enter password: `z4jfLsJZHPSJQLzE5q2c`

### Step 2: Download SQL File

```bash
scp denncath@da11.host-africa.com:~/public_html/products.sql ~/grocery-ecommerce/
```

### Step 3: Import to Local MySQL

```bash
cd ~/grocery-ecommerce
mysql -u root -p grocery_db < products.sql
```

Enter your local MySQL password.

---

## What Gets Synced?

✅ **Categories**: All product categories (Vegetables, Fruits, Eggs and Dairy, etc.)  
✅ **Products**: All products with prices, descriptions, stock, and images

⚠️ **Note**: Product images are stored in `/static/images/` - make sure to sync those separately if needed:

```bash
# Sync images from production
scp -r denncath@da11.host-africa.com:~/public_html/static/images/* ~/grocery-ecommerce/static/images/
```

---

## Troubleshooting

**Can't connect to production database remotely?**
- Use Method 1 (SSH + JSON export) instead
- Host Africa may block remote MySQL connections

**Import fails with foreign key errors?**
- The scripts import categories first, then products
- Make sure your local database is empty or run: `flask db upgrade`

**Products show but no images?**
- Sync the `/static/images/` directory from production (see note above)

---

## Files Created

- `export_to_json.py` - Run on production to create JSON export
- `import_from_json.py` - Run locally to import from JSON
- `sync_products_from_production.py` - Direct database sync (if remote access allowed)
- `export_products_from_production.sh` - Bash script for SQL dump

---

## Quick Reference

```bash
# On Production Server
python3 export_to_json.py

# On Local Machine
scp denncath@da11.host-africa.com:~/public_html/products_export.json .
python3 import_from_json.py
```

That's it! Your local database now has all production products! 🚀
