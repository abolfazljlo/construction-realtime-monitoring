import os
import ssl
import smtplib
import asyncio
from email.message import EmailMessage
from .base import EmailProvider
from ....utils.log import Log

class SMTPProvider(EmailProvider):
    """
    Basic SMTP provider.

    Reads configuration from environment variables:

        SMTP_HOST       (default: "localhost")
        SMTP_PORT       (default: 587)
        SMTP_USERNAME   (optional)
        SMTP_PASSWORD   (optional)
        SMTP_USE_TLS    (default: "true")
        SMTP_FROM       (default: SMTP_USERNAME or "no-reply@example.com")
        SMTP_TIMEOUT    (default: 10)

    """

    def __init__(self):
        self.host = os.getenv("SMTP_HOST", "localhost")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.timeout = int(os.getenv("SMTP_TIMEOUT", "10"))
        self.from_email = os.getenv("SMTP_FROM", self.username or "no-reply@example.com")
        
    async def send(self, message) -> None:

        email = EmailMessage()
        email["From"] = self.from_email
        email["To"] = message.data.to
        email["Subject"] = message.data.subject
        email.set_content(message.data.body)

        Log.info(
            f"[SMTPProvider] Sending email → {message.data.to} "
            f"(subject='{message.data.subject}')"
        )

        def _send_sync():
            try:
                if self.use_tls:
                    context = ssl.create_default_context()
                    with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as smtp:
                        smtp.starttls(context=context)
                        if self.username and self.password:
                            smtp.login(self.username, self.password)
                        smtp.send_message(email)
                else:
                    with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as smtp:
                        if self.username and self.password:
                            smtp.login(self.username, self.password)
                        smtp.send_message(email)

            except Exception as e:
                raise RuntimeError(f"SMTP error: {e}") from e

        # Run blocking SMTP inside a thread so it won't block your async loop
        await asyncio.to_thread(_send_sync)

        Log.success(f"[SMTPProvider] Email sent → {message.data.to}")
