import os
import pandas as pd
import ssl
import smtplib
import imaplib
import email
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import random
import time
import json
def send_email(to_address, subject, body, from_address, password):
   
    context = smtplib.ssl.create_default_context()
    message = MIMEMultipart()
    message["From"] = from_address
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_address, password)
            server.sendmail(from_address, to_address, message.as_string())
            print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Error sending email to {to_address}: {e}")

def email_summaries_to_users(news_summaries, users_emails, from_address, password):
    subject = "Tech News Summaries"

    for name, email in users_emails.items():
        body = f"Hello {name},\n\nHere are your tech news summaries:\n"
        for summary in news_summaries:
            body += f"\nTitle: {summary['title']}\nSummary: {summary['summary']}\n"
        send_email(email, subject, body, from_address, password)

users_emails = {"rafey": os.getenv('EMAIL')}
from_address = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


email_summaries_to_users(get_tech_news(10), users_emails, from_address, password)
