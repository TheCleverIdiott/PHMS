# modules/notifier.py

from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
import streamlit as st

# --- SMS via Twilio ---
def send_sms_alert(message):
    try:
        client = Client(st.secrets["TWILIO_SID"], st.secrets["TWILIO_AUTH_TOKEN"])
        client.messages.create(
            body=message,
            from_=st.secrets["TWILIO_FROM_NUMBER"],
            to=st.secrets["USER_PHONE"]
        )
        print("✅ SMS alert sent.")
    except Exception as e:
        print(f"❌ SMS failed: {e}")

# --- Email via Gmail SMTP ---
def send_email_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = st.secrets["EMAIL"]
        msg["To"] = st.secrets["USER_EMAIL"]

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(st.secrets["EMAIL"], st.secrets["EMAIL_PASSWORD"])
            server.send_message(msg)
        print("✅ Email alert sent.")
    except Exception as e:
        print(f"❌ Email failed: {e}")
