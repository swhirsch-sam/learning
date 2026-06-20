"""Send the daily digest as an HTML email using only the Python standard library.

No third-party email service or SDK — just ``smtplib`` over SSL, configured
through environment variables. For Gmail, ``EMAIL_APP_PASSWORD`` must be an app
password (2-factor auth required); a regular account password will not work.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject: str, html_body: str) -> None:
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_APP_PASSWORD")
    recipient = os.environ.get("EMAIL_RECIPIENT")
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))

    missing = [
        name
        for name, value in (
            ("EMAIL_SENDER", sender),
            ("EMAIL_APP_PASSWORD", password),
            ("EMAIL_RECIPIENT", recipient),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing required email environment variables: " + ", ".join(missing)
        )

    # EMAIL_RECIPIENT may be a single address or a comma-separated list.
    recipients = [addr.strip() for addr in recipient.split(",") if addr.strip()]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, message.as_string())
