#!/bin/bash
# Export Products from Production Database
# Run this script on Host Africa server to export product data

echo "🚀 Exporting Products from Production Database"
echo "=============================================="

# Database credentials
DB_USER="denncath_flaskapp"
DB_NAME="denncath_flaskapp"
OUTPUT_FILE="products_export.sql"

echo ""
echo "📦 Exporting categories and products..."

# Export only category and product tables
mysqldump -u $DB_USER -p $DB_NAME category product > $OUTPUT_FILE

if [ $? -eq 0 ]; then
    echo "✅ Export successful!"
    echo "📁 File created: $OUTPUT_FILE"
    echo ""
    echo "📥 To download to your local machine, run:"
    echo "   scp denncath@da11.host-africa.com:~/public_html/$OUTPUT_FILE ."
    echo ""
    echo "📥 Then import to local database:"
    echo "   mysql -u root -p grocery_db < $OUTPUT_FILE"
else
    echo "❌ Export failed!"
fi
