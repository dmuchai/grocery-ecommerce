
import unittest
from flask import Flask
from models import db, Order, EmailQueue
from routes.payment import payment_bp
from process_emails import process_email_queue
from unittest.mock import patch, MagicMock

class TestAsyncEmailFlow(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()
            
            # Create dummy order
            self.order = Order(
                merchant_reference='ASYNC_TEST_123',
                email='async_test@example.com',
                customer_name='Async User',
                address='123 Test St',
                total_price=100.0,
                status='pending'
            )
            db.session.add(self.order)
            db.session.commit()
            self.order_id = self.order.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_queue_creation_and_processing(self):
        """Test that jobs are queued and then processed"""
        with self.app.app_context():
            # 1. Manually enqueue jobs (simulating payment_callback)
            queue_item = EmailQueue(
                order_id=self.order_id,
                email_type='order_confirmation',
                recipient='async_test@example.com',
                status='pending'
            )
            db.session.add(queue_item)
            db.session.commit()
            
            # Verify pending
            stored_job = db.session.get(EmailQueue, queue_item.id)
            self.assertEqual(stored_job.status, 'pending')
            
            # 2. Run Worker (Mocking the actual send function to avoid SMTP)
            # Patch the 'app' object imported in process_emails to use our test app
            with patch('process_emails.send_order_confirmation_email') as mock_send, \
                 patch('process_emails.app', self.app):
                
                process_email_queue()
                
                mock_send.assert_called_once()
                
                # 3. Verify status changed to sent
                # Force refresh from DB since process_emails committed a transaction
                db.session.expire_all()
                updated_job = db.session.get(EmailQueue, queue_item.id)
                self.assertEqual(updated_job.status, 'sent')
                self.assertIsNotNone(updated_job.sent_at)

if __name__ == '__main__':
    unittest.main()
