# ============================================================
# PATIENTCONNECT - MAILTRAP SMTP EMAIL INTEGRATION
# File: mailer.py
# ============================================================

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GET MAILTRAP CONFIGURATION
# ============================================================

def get_mail_config():
    """
    Read Mailtrap SMTP configuration from .env
    """

    host = os.getenv("MAILTRAP_SMTP_HOST")
    port = os.getenv("MAILTRAP_SMTP_PORT")
    username = os.getenv("MAILTRAP_SMTP_USERNAME")
    password = os.getenv("MAILTRAP_SMTP_PASSWORD")

    sender_email = os.getenv(
        "MAILTRAP_SENDER_EMAIL",
        "hello@example.com"
    )

    sender_name = os.getenv(
        "MAILTRAP_SENDER_NAME",
        "PatientConnect"
    )

    if not host:
        raise RuntimeError(
            "MAILTRAP_SMTP_HOST is missing from .env"
        )

    if not port:
        raise RuntimeError(
            "MAILTRAP_SMTP_PORT is missing from .env"
        )

    if not username:
        raise RuntimeError(
            "MAILTRAP_SMTP_USERNAME is missing from .env"
        )

    if not password:
        raise RuntimeError(
            "MAILTRAP_SMTP_PASSWORD is missing from .env"
        )

    return {
        "host": host,
        "port": int(port),
        "username": username,
        "password": password,
        "sender_email": sender_email,
        "sender_name": sender_name,
    }


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(
    to_email,
    subject,
    text,
    html=None,
    to_name=None
):
    """
    Send an email through Mailtrap SMTP.

    Returns:
        True  -> email sent successfully
        False -> email failed
    """

    if not to_email:
        print("[mailer] No recipient email provided.")
        return False

    try:

        config = get_mail_config()

        # ----------------------------------------------------
        # CREATE EMAIL
        # ----------------------------------------------------

        message = EmailMessage()

        message["Subject"] = subject

        message["From"] = (
            f"{config['sender_name']} "
            f"<{config['sender_email']}>"
        )

        message["To"] = (
            f"{to_name} <{to_email}>"
            if to_name
            else to_email
        )

        # Plain text version
        message.set_content(text)

        # HTML version
        if html:
            message.add_alternative(
                html,
                subtype="html"
            )

        # ----------------------------------------------------
        # CONNECT TO MAILTRAP SMTP
        # ----------------------------------------------------

        print(
            f"[mailer] Connecting to "
            f"{config['host']}:{config['port']}..."
        )

        with smtplib.SMTP(
            config["host"],
            config["port"]
        ) as server:

            # STARTTLS encryption
            server.starttls()

            # Login
            server.login(
                config["username"],
                config["password"]
            )

            # Send email
            server.send_message(message)

        print(
            f"[mailer] Email sent successfully "
            f"to {to_email}"
        )

        return True

    except Exception as e:

        print(
            f"[mailer] Failed to send email "
            f"to {to_email}: {e}"
        )

        return False


# ============================================================
# TEST MAILER
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("     PATIENTCONNECT MAILTRAP TEST")
    print("========================================\n")

    test_email = input(
        "Enter recipient email: "
    ).strip()

    success = send_email(
        to_email=test_email,
        to_name="Test Patient",
        subject="PatientConnect Test Email",
        text=(
            "Hello!\n\n"
            "This is a test email from "
            "PatientConnect.\n\n"
            "Mailtrap SMTP integration is working."
        ),
        html="""
        <html>
            <body>
                <h2>PatientConnect</h2>

                <p>Hello!</p>

                <p>
                    This is a test email from
                    <strong>PatientConnect</strong>.
                </p>

                <p>
                    Mailtrap SMTP integration
                    is working successfully.
                </p>
            </body>
        </html>
        """
    )

    if success:
        print("\n✅ Mailtrap test successful.")
        print("Check your Mailtrap Sandbox inbox.")

    else:
        print("\n❌ Mailtrap test failed.")