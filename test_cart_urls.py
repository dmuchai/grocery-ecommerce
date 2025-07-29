#!/usr/bin/env python3
"""
Test script to debug the cart-data image URL issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Product

def test_cart_data_urls():
    """Test and debug the cart-data URL issue"""
    
    with app.test_client() as client:
        with app.app_context():
            print("🧪 Testing Cart-Data URL Processing...")
            
            # Create a test product first
            test_product = Product(
                name="Test Watermelon",
                description="Test product for debugging",
                price=60.0,
                stock=10,
                image_url="watermelon.jpg",  # Just the filename
                category_id=1
            )
            
            try:
                db.session.add(test_product)
                db.session.commit()
                product_id = test_product.id
                print(f"✅ Created test product with ID {product_id}")
                
                # Simulate adding to cart
                with client.session_transaction() as sess:
                    sess['cart'] = {
                        str(product_id): {
                            'id': product_id,
                            'name': 'Test Watermelon',
                            'image_url': 'watermelon.jpg',  # Original filename
                            'price': 60.0,
                            'quantity': 1
                        }
                    }
                
                print("✅ Added item to cart session")
                
                # Test cart-data endpoint multiple times to see URL evolution
                for i in range(3):
                    print(f"\n🔄 Cart-data call #{i+1}:")
                    response = client.get('/cart-data')
                    
                    if response.status_code == 200:
                        data = response.get_json()
                        if 'items' in data and data['items']:
                            image_url = data['items'][0].get('image_url', 'MISSING')
                            print(f"   Image URL: {image_url}")
                        else:
                            print("   No items in response")
                    else:
                        print(f"   Error: {response.status_code}")
                
                # Cleanup
                db.session.delete(test_product)
                db.session.commit()
                print("✅ Cleaned up test product")
                
                return True
                
            except Exception as e:
                print(f"❌ Test failed: {e}")
                try:
                    db.session.rollback()
                    if 'test_product' in locals():
                        db.session.delete(test_product)
                        db.session.commit()
                except:
                    pass
                return False

if __name__ == "__main__":
    if test_cart_data_urls():
        print("\n✅ Cart-data URL test completed!")
        sys.exit(0)
    else:
        print("\n❌ Cart-data URL test failed!")
        sys.exit(1)
