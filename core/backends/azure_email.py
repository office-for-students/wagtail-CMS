"""SMTP email backend class."""
import logging

from azure.communication.email import EmailClient
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.core.mail.backends.base import BaseEmailBackend

import threading

class OFSEmailBackend(BaseEmailBackend):
    """
    A wrapper that manages the SMTP network connection.
    """

    def __init__(
            self,
            connection_string=None,
            fail_silently=False,
            email_client=None,
            **kwargs,
    ):
        super().__init__(fail_silently=fail_silently)
        self.email_client = None
        try:
            self.connection_string = connection_string or settings.AZURE_EMAIL_SERVICE_CONNECTION_STRING
            self.email_client = email_client or EmailClient.from_connection_string(self.connection_string)
        except ImproperlyConfigured:
            if not self.fail_silently:
                raise ImproperlyConfigured(
                    "Email backend requires: AZURE_EMAIL_SERVICE_CONNECTION_STRING in settings.py")

    # def open(self):
    #     print("open wide")
    #
    #     pass
    #
    # def close(self):
    #     print("close now")
    #     pass
    #
    # def __enter__(self):
    #     try:
    #         self.open()
    #     except Exception:
    #         self.close()
    #         raise
    #     return self
    #
    # def __exit__(self, exc_type, exc_value, traceback):
    #     self.close()

    def send_messages(self, email_messages: EmailMessage, **kwargs):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        def send():
            if not settings.DEBUG:
                for message in email_messages:
                    try:
                        if message.alternatives and message.alternatives[0].content:
                            html_message = message.alternatives[0].content
                        else:
                            html_message = message.body
                    except (IndexError, AttributeError):
                        html_message = message.body

                    email_content = {
                        "senderAddress": settings.AZURE_EMAIL_OUTGOING_EMAIL_ADDRESS,
                        "recipients": {
                            "to": [{"address": x} for x in message.to]
                        },
                        "content": {
                            "subject": f"[{settings.AZURE_EMAIL_SERVICE_ENVIRONMENT} - DU]  {message.subject}",
                            "plainText": message.body,
                            "html": html_message,
                        },
                    }

                    poller = self.email_client.begin_send(email_content)
                    result = poller.result()
                else:
                    logging.info(f"No Email message sent in DEBUG: {settings.DEBUG}. Message not sent: {email_content}.")

        thread = threading.Thread(target=send)
        thread.daemon = True
        thread.start()