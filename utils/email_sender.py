import os
import requests
import traceback
import sys


def send_contact_notification(name, email, phone, message):
    try:
        api_key = os.getenv("BREVO_API_KEY")
        if not api_key:
            print("Brevo API key missing in environment")
            return False

        sender_email = os.getenv("MAIL_DEFAULT_SENDER")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "chourasiavarun16@gmail.com")

        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key
        }
        data = {
            "sender": {"name": "Portfolio Contact", "email": sender_email},
            "to": [{"email": recipient_email, "name": "You"}],
            "subject": f"New Portfolio Contact: {name}",
            "htmlContent": f"""
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
            """,
            "textContent": f"""
                New Contact Form Submission
                
                Name: {name}
                Email: {email}
                Phone: {phone}

                Message:
                {message}
            """
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            print("✅ Email sent successfully using Brevo API")
            return True
        else:
            print("❌ Failed to send email via Brevo API:", response.text)
            return False

    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        print("Email sending failed:", str(e), file=sys.stderr)
        return False
