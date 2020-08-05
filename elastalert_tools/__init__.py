import os

def send_email(sender, receiver, msg):
    with smtplib.SMTP_SSL(os.environ['SMTP_SERVER']) as server:
        server.sendmail(sender, receiver, msg)
        server.quit()