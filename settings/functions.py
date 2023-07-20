import aiosmtplib
from .vars import EMAIL_HOST, EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_TO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_email(subject, message, message_html):
    smtp = aiosmtplib.SMTP(
        hostname=EMAIL_HOST, port=EMAIL_PORT,
        use_tls=True
    )
    await smtp.connect()

    email = MIMEMultipart("alternative")
    email["From"] = EMAIL_LOGIN
    email["To"] = EMAIL_TO
    email["Subject"] = subject
    email.attach(MIMEText(message, "plain"))
    email.attach(MIMEText(message_html, "html"))

    await smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    await smtp.send_message(email)
    await smtp.quit()
