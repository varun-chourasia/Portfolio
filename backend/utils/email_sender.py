from flask_mail import Mail, Message
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mail = Mail()

def send_contact_notification(name, email, message):
    """Send email notification when contact form is submitted"""
    try:
        recipient = current_app.config.get('MAIL_USERNAME')
        
        if not recipient:
            print("Email configuration missing")
            return False
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'New Portfolio Contact: {name}'
        msg['From'] = current_app.config.get('MAIL_DEFAULT_SENDER')
        msg['To'] = recipient
        
        # Email body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #00d9ff;">New Contact Form Submission</h2>
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Message:</strong></p>
                    <p style="background-color: white; padding: 15px; border-left: 4px solid #00d9ff;">
                        {message}
                    </p>
                </div>
                <p style="color: #666; font-size: 12px; margin-top: 20px;">
                    This email was sent from your portfolio contact form.
                </p>
            </body>
        </html>
        """
        
        text = f"""
        New Contact Form Submission
        
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], 
                         current_app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'],
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False
