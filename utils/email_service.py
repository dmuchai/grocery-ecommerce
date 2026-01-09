"""Email service for sending transactional emails"""
from flask_mail import Mail, Message
from flask import render_template, current_app
import logging

mail = Mail()
logger = logging.getLogger(__name__)


def send_email(subject, recipients, html_body, text_body=None):
    """Generic email sending function"""
    try:
        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            html=html_body,
            body=text_body
        )
        mail.send(msg)
        logger.info(f"Email sent to {recipients} with subject: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipients}: {e}", exc_info=True)
        return False


def send_order_confirmation_email(order, customer_email):
    """Send order confirmation to customer"""
    try:
        subject = f"Order Confirmation - {order.merchant_reference}"
        html_body = render_template('emails/order_confirmation.html', order=order)
        
        return send_email(
            subject=subject,
            recipients=[customer_email],
            html_body=html_body
        )
    except Exception as e:
        logger.error(f"Failed to render order confirmation email: {e}", exc_info=True)
        return False


def send_new_order_alert_to_admin(order):
    """Alert admin of new order"""
    try:
        subject = f"New Order Received - {order.merchant_reference}"
        html_body = render_template('emails/admin_new_order.html', order=order)
        
        return send_email(
            subject=subject,
            recipients=[current_app.config['ADMIN_EMAIL']],
            html_body=html_body
        )
    except Exception as e:
        logger.error(f"Failed to render admin alert email: {e}", exc_info=True)
        return False


def send_payment_received_email(order):
    """Confirm payment received"""
    try:
        subject = f"Payment Received - {order.merchant_reference}"
        html_body = render_template('emails/payment_received.html', order=order)
        
        return send_email(
            subject=subject,
            recipients=[order.email],
            html_body=html_body
        )
    except Exception as e:
        logger.error(f"Failed to render payment received email: {e}", exc_info=True)
        return False


def send_order_shipped_email(order):
    """Notify customer order has shipped"""
    try:
        subject = f"Your Order Has Shipped - {order.merchant_reference}"
        html_body = render_template('emails/order_shipped.html', order=order)
        
        return send_email(
            subject=subject,
            recipients=[order.email],
            html_body=html_body
        )
    except Exception as e:
        logger.error(f"Failed to render shipment email: {e}", exc_info=True)
        return False


def send_order_cancelled_email(order):
    """Notify customer order has been cancelled"""
    try:
        subject = f"Order Cancelled - {order.merchant_reference}"
        html_body = render_template('emails/order_cancelled.html', order=order)
        
        return send_email(
            subject=subject,
            recipients=[order.email],
            html_body=html_body
        )
    except Exception as e:
        logger.error(f"Failed to render cancellation email: {e}", exc_info=True)
        return False


def send_payment_failed_email(order):
    """Notify customer payment failed and allow retry"""
    try:
        subject = f"Payment Failed - Action Required - {order.merchant_reference}"
        html_body = render_template('emails/payment_failed.html', order=order)
        
        return send_email(
            subject=subject,
            recipients=[order.email],
            html_body=html_body
        )
    except Exception as e:
        logger.error(f"Failed to render payment failed email: {e}", exc_info=True)
        return False
