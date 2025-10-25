from flask_mail import Mail, Message
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback, sys


mail = Mail()


def send_contact_notification(name, email, phone, message):
    """Send email notification when contact form is submitted"""
    try:
        # CHANGE THIS: Send to your Gmail, not MAIL_USERNAME
        recipient = 'chourasiavarun16@gmail.com'  # YOUR GMAIL ADDRESS
        
        if not recipient:
            print("Email configuration missing")
            return False
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'New Portfolio Contact: {name}'
        msg['From'] = current_app.config.get('MAIL_DEFAULT_SENDER')
        msg['To'] = recipient
        msg['Reply-To'] = email
        
        # Email body
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #00d9ff;">New Contact Form Submission</h2>
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Number:</strong> {phone}</p>
                    
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
        Phone: {phone}

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
        
        print(f"✅ Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        print("Email sending failed:", str(e), file=sys.stderr)
        return False
