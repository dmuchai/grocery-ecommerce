#!/usr/bin/env python3
"""
Test script to verify URL cleanup for corrupted cart data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_corrupted_cart_cleanup():
    """Test cleanup of corrupted cart URLs"""
    
    with app.test_client() as client:
        with app.app_context():
            print("🧪 Testing Corrupted Cart URL Cleanup...")
            
            # Simulate corrupted cart data
            with client.session_transaction() as sess:
                sess['cart'] = {
                    '6': {
                        'id': 6,
                        'name': 'Test Watermelon',
                        'image_url': 'http://127.0.0.1:5000/static/images/http://127.0.0.1:5000/static/images/watermelon.jpg',
                        'price': 60.0,
                        'quantity': 1
                    },
                    '2': {
                        'id': 2,
                        'name': 'Test Pineapples',
                        'image_url': '/static/images/pineapples.jpg',  # Already clean
                        'price': 80.0,
                        'quantity': 1
                    }
                }
            
            print("✅ Added corrupted cart data to session")
            
            # Test cart-data cleanup
            print("\n🔄 Testing cart-data with corrupted URLs:")
            response = client.get('/cart-data')
            
            if response.status_code == 200:
                data = response.get_json()
                for item in data.get('items', []):
                    name = item.get('name', 'Unknown')
                    image_url = item.get('image_url', 'MISSING')
                    print(f"   {name}: {image_url}")
                    
                    # Check if URLs are properly cleaned
                    if 'http://127.0.0.1:5000/static/images/http://' in image_url:
                        print(f"   ❌ URL still corrupted for {name}")
                        return False
                    elif image_url.startswith('/static/images/') and not 'http://127.0.0.1:5000' in image_url:
                        print(f"   ✅ URL properly cleaned for {name}")
                    else:
                        print(f"   ⚠️  Unexpected URL format for {name}")
                
            # Test cart cleaning endpoint
            print("\n🔄 Testing cart/clean endpoint:")
            response = client.get('/cart/clean')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"   {data.get('message', 'No message')}")
                
                # Check cleaned cart
                cart = data.get('cart', {})
                for product_id, item in cart.items():
                    name = item.get('name', 'Unknown')
                    image_url = item.get('image_url', 'MISSING')
                    print(f"   Cleaned {name}: {image_url}")
                    
                    if 'http' in image_url:
                        print(f"   ❌ Cleaning failed for {name}")
                        return False
            
            print("\n✅ All corruption cleanup tests passed!")
            return True

if __name__ == "__main__":
    if test_corrupted_cart_cleanup():
        print("\n✅ Corrupted cart cleanup test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Corrupted cart cleanup test failed!")
        sys.exit(1)
