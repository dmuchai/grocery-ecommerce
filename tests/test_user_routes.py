import unittest
from tests.base import BaseTestCase
from models import db

class TestUserRoutes(BaseTestCase):
    """Test cases for user registration and authentication."""
    
    def test_user_registration_success(self):
        """Test successful user registration."""
        response = self.app.post('/user/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'SecurePass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
    
    def test_user_registration_weak_password(self):
        """Test registration with weak password."""
        response = self.app.post('/user/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'weak'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_user_registration_invalid_email(self):
        """Test registration with invalid email."""
        response = self.app.post('/user/register', data={
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'SecurePass123'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_duplicate_email_registration(self):
        """Test registration with existing email."""
        self.create_user(email='existing@example.com')
        
        response = self.app.post('/user/register', data={
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'SecurePass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login

if __name__ == '__main__':
    unittest.main()
