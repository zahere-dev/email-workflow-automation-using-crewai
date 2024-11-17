#!/usr/bin/env python
import os
import sys
import time

from crew import AgentCrew
from tools.email_ops import read_emails, send_email

from dotenv import load_dotenv

load_dotenv()


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    while (True):
        time.sleep(3)

        print("Reading emails...")
        emails = read_emails()

        if not emails:
            continue

        latest_email = emails[0]

        sender_email = [header['value'] for header in latest_email['headers'] if header['name'] == 'From'][0]
        email_subject = [header['value'] for header in latest_email['headers'] if header['name'] == 'Subject'][0]
        email_body = latest_email['snippet']

        email_input = f"""
        Sender_Email: {sender_email} 
        Subject: {email_subject}
        Body: {email_body}
        """

        print("Email content:", email_input)

        inputs = {
            'email_content': email_input
        }
        AgentCrew().crew().kickoff(inputs=inputs)

        # Stop the loop after a successful run (should only run once for the demo)
        # Remove this if you want the loop to run forever
        break


run()
