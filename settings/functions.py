from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from .vars import EMAIL_HOST, EMAIL_LOGIN, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_TO


async def send_email(subject, message, message_html):
    """Функция отправки E-mail

    Args:
        subject (_type_): Тема письма
        message (_type_): Само письмо
        message_html (_type_): Письмо в формате HTML
    """
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
