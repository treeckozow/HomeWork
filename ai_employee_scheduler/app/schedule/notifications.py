# app/notifications.py
import os
import http.client
import json
from email.message import EmailMessage

def send_email(recipient: str, subject: str, body: str):
    """
    Sends an email using the SendGrid API.
    Make sure you set the following environment variables:
      - RESEND_API_KEY: your SendGrid API key.
      - SENDER_EMAIL: your verified sender email address.
    """
    # Retrieve credentials from environment variables
    api_key = os.getenv("RESEND_API_KEY") # "re_GHoane99_PLKf3LZRhWoviw376qVMs49u" # <-- Replace or set env var
    sender_email = os.getenv("SENDER_EMAIL") # "treeckozow@gmail.com" # <-- Replace or set env var

    if not api_key or not sender_email:
        raise Exception("RESEND_API_KEY and SENDER_EMAIL must be set in your environment variables.")

    conn = http.client.HTTPSConnection("api.sendgrid.com")
    
    payload = json.dumps({
        "personalizations": [
            {
                "to": [
                    {
                        "email": recipient
                    }
                ]
            }
        ],
        "from": {
            "email": sender_email
        },
        "subject": subject,
        "content": [
            {
                "type": "text/plain",
                "value": body
            }
        ]
    })

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/v3/mail/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def send_notification(recipient_contact: str, message: str):
    """
    Sends a notification using Email (and optionally SMS).
    Extend this function as needed.
    """
    subject = "Employee Scheduling Notification"
    send_email(recipient_contact, subject, message)
    # Optionally, if recipient_contact is a phone number, call send_sms()
