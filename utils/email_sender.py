import os
import requests
import traceback
import sys


def send_contact_notification(name, email, phone, message):
    try:
        api_key = os.getenv("BREVO_API_KEY")
        if not api_key:
            print("❌ Missing Brevo API key in environment")
            return False

        sender_email = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@example.com")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "chourasiavarun16@gmail.com")

        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key
        }

        data = {
            "sender": {"name": "Portfolio Contact", "email": sender_email},
            "to": [{"email": recipient_email, "name": "Varun"}],
            "subject": f"📬 New Portfolio Contact from {name}",
            "htmlContent": f"""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <h2 style="color:#00d9ff;">New Contact Form Submission</h2>
                        <div style="background:#f9f9f9;padding:15px;border-radius:5px;">
                            <p><strong>Name:</strong> {name}</p>
                            <p><strong>Email:</strong> {email}</p>
                            <p><strong>Phone:</strong> {phone}</p>
                            <p><strong>Message:</strong></p>
                            <div style="background:white;padding:10px;border-left:3px solid #00d9ff;">
                                {message}
                            </div>
                        </div>
                        <p style="font-size:12px;color:#666;margin-top:20px;">
                            — Sent automatically from your Portfolio Website
                        </p>
                    </body>
                </html>
            """,
            "replyTo": {"email": email, "name": name}
        }

        print("📤 Sending email via Brevo API...")
        response = requests.post(url, json=data, headers=headers, timeout=10)

        print(f"✅ Brevo Response: {response.status_code}")
        print(response.text)

        # Brevo API returns 201 if successfully queued
        if response.status_code == 201:
            print("🎉 Email sent successfully!")
            return True
        else:
            print(f"⚠️ Email failed: {response.text}")
            return False

    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        print("❌ Email sending failed:", str(e), file=sys.stderr)
        return False
