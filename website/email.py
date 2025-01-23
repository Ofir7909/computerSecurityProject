import smtplib
from django.conf import settings


def send_email(toMail, subject, message):
    fromMail = f"Computer Security Project <{settings.MAIL}>"
    message = f"""\
Subject: {subject}
To: {toMail}
From: {fromMail}

{message}
"""

    try:
        with smtplib.SMTP(settings.SMTP_URL, 587) as server:
            server.starttls()
            server.login("api", settings.MAIL_PASS)
            server.sendmail(fromMail, toMail, message)
    except Exception as e:
        print(e)
