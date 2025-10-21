import re

def validate_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove spaces, dashes, and parentheses
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if it's all digits and reasonable length
    if cleaned.isdigit() and 10 <= len(cleaned) <= 15:
        return True
    return False

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return ''
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '`']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def validate_message_length(message, min_length=10, max_length=1000):
    """Validate message length"""
    if not message:
        return False
    
    length = len(message.strip())
    return min_length <= length <= max_length
