from app import app
from models import db
from models.email_queue import EmailQueue
from models.order import Order
from utils.email_service import (
    send_order_confirmation_email,
    send_new_order_alert_to_admin,
    send_payment_received_email
)
from datetime import datetime
import traceback
import sys

def process_email_queue():
    """Fetch pending emails and send them"""
    with app.app_context():
        print(f"[{datetime.now()}] Checking email queue...")
        
        # Fetch pending jobs or failed jobs with < 5 attempts
        jobs = EmailQueue.query.filter(
            (EmailQueue.status == 'pending') | 
            ((EmailQueue.status == 'failed') & (EmailQueue.attempts < 5))
        ).all()
        
        if not jobs:
            print("No pending emails found.")
            return

        print(f"Found {len(jobs)} emails to process.")

        for job in jobs:
            try:
                print(f"Processing Job #{job.id} (Type: {job.email_type}, Order: {job.order_id})...")
                
                # Mark as processing
                job.status = 'processing'
                db.session.commit()
                
                # Fetch fresh order data
                order = db.session.get(Order, job.order_id)
                if not order:
                    raise ValueError(f"Order {job.order_id} not found")

                # Send email based on type
                if job.email_type == 'order_confirmation':
                    send_order_confirmation_email(order, job.recipient)
                elif job.email_type == 'new_order_admin':
                    send_new_order_alert_to_admin(order)
                elif job.email_type == 'payment_received':
                    send_payment_received_email(order)
                else:
                    raise ValueError(f"Unknown email type: {job.email_type}")

                # Success
                job.status = 'sent'
                job.sent_at = datetime.utcnow()
                job.last_error = None
                print(f"✅ Job #{job.id} sent successfully.")

            except Exception as e:
                # Failure
                job.attempts += 1
                job.last_error = str(e) + "\n" + traceback.format_exc()
                
                if job.attempts >= 5:
                    job.status = 'failed_permanent'
                    print(f"❌ Job #{job.id} failed permanently after 5 attempts.")
                else:
                    job.status = 'failed'
                    print(f"⚠️ Job #{job.id} failed (Attempt {job.attempts}). Retrying later.")
                
            # Commit after each job to save progress
            db.session.commit()

if __name__ == "__main__":
    process_email_queue()
