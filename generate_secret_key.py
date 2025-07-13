#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for Flask applications
Run this script to generate a new secret key for production
"""
import secrets

def generate_secret_key():
    """Generate a cryptographically secure secret key."""
    return secrets.token_hex(32)

if __name__ == "__main__":
    key = generate_secret_key()
    print("Generated SECRET_KEY:")
    print(key)
    print("\nAdd this to your production .env file:")
    print(f"SECRET_KEY={key}")
