import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required to read, compose, and send emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


def authenticate_gmail():
    creds = None
    # Use the refresh token and client secrets to generate credentials
    REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")
    if REFRESH_TOKEN:
        creds = Credentials(
            token=None,
            refresh_token=REFRESH_TOKEN,
            client_id=os.getenv("GMAIL_CLIENT_ID"),
            client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
            token_uri=os.getenv("GMAIL_TOKEN_URI")
        )

    # If credentials are not valid, force re-authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    return creds


def read_emails():
    try:
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)

        # Get the list of messages
        results = service.users().messages().list(userId='me', maxResults=5, q="is:unread").execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            email_body = msg['snippet']
            emails.append({'headers': email_data, 'snippet': email_body})
        return emails

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def send_email(to, subject, message_text):
    try:
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)

        # Create a MIMEText email
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(message_text, 'plain'))

        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}

        # Send the email
        message = service.users().messages().send(userId='me', body=body).execute()
        print(f"Message sent with ID: {message['id']}")

    except HttpError as error:
        print(f'An error occurred: {error}')

