from flask import Blueprint, request, jsonify
from models import db, ContactMessage
from utils.validators import validate_email, validate_phone
from utils.email_sender import send_contact_notification
import threading
import re


contact_bp = Blueprint('contact', __name__)


def send_email_async(name, email, phone, message):
    """Send email in background thread to avoid blocking"""
    thread = threading.Thread(
        target=send_contact_notification,
        args=(name, email, phone, message)
    )
    thread.daemon = True
    thread.start()


@contact_bp.route('/submit', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        phone = data.get('phone', '').strip()
        
        # Validation
        if not name or len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email address'}), 400
        
        if not message or len(message) < 5:
            return jsonify({'error': 'Message must be at least 10 characters'}), 400
        
        if phone and not validate_phone(phone):
            return jsonify({'error': 'Invalid phone number'}), 400
        
        # Create new contact message
        contact = ContactMessage(
            name=name,
            email=email,
            phone=phone if phone else None,
            message=message
        )
        
        db.session.add(contact)
        db.session.commit()
        
        # Send email notification in background (non-blocking)
        try:
            send_email_async(name, email, phone, message)
        except Exception as e:
            print(f"Email notification failed: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! I will get back to you soon.',
            'data': contact.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@contact_bp.route('/messages', methods=['GET'])
def get_messages():
    """Get all contact messages (admin only - add authentication)"""
    try:
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        return jsonify({
            'success': True,
            'count': len(messages),
            'messages': [msg.to_dict() for msg in messages]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@contact_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
def mark_as_read(message_id):
    """Mark message as read (admin only - add authentication)"""
    try:
        message = ContactMessage.query.get_or_404(message_id)
        message.is_read = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'Message marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
