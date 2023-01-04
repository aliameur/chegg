from imaplib import IMAP4_SSL
import asyncio
import email
import re
import time

TIMEOUT = 10


def connect_email(_email: str, password: str) -> IMAP4_SSL:
    """
    Connect to mail object and login. Email and password from env.
    :param _email:
    :param password:
    :return:
    """
    # Connect to the server
    mail = IMAP4_SSL('imap.gmail.com')
    # Login to your account
    mail.login(_email, password)
    # Select the mailbox you want to read from
    mail.select('inbox')
    return mail


def search_email(mail: IMAP4_SSL) -> str:
    """
    Search for unread emails from homeworkify and parse them to return the one-use link. May raise TimeoutError.
    :param mail:
    :return: solution link to screenshot
    """

    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        # Search for all unread messages and return their IDs
        status, data = mail.search(None, 'UNSEEN')
        # If there are any unread messages
        if status == 'OK':
            # Loop through the message IDs
            for msg_id in data[0].split():
                # Fetch the full message
                status, msg = mail.fetch(msg_id, "(RFC822)")
                if status == 'OK':
                    # Parse the message into a message object
                    msg = email.message_from_bytes(msg[0][1])
                    # Extract the links from the message
                    if "support@homeworkify.net" in msg["From"]:
                        for part in msg.walk():
                            if part.get_content_type() == 'text/html':
                                html = part.get_payload()
                                link = re.search(r'<a href="(https?://\S+)">', html)
                                return link.group(1)
        asyncio.sleep(1)
    raise TimeoutError("Timed out while waiting for confirmation email.")


def close_email(mail: IMAP4_SSL) -> None:
    """
    closes mail object's connection
    :param mail:
    :return:
    """
    mail.close()
    mail.logout()
