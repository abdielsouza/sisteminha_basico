import smtplib
from email.mime.text import MIMEText
from myutil import *

def send_email(subject, body, email, recipients, password):
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        
        smtp_server.ehlo()

        try:
            smtp_server.login(email, password)
            smtp_server.sendmail(email, recipients, msg.as_string())
        except Exception as e:
            add_out_message(e)
            return
