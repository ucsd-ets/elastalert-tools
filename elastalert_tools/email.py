import email.mime.text, email.mime.multipart, smtplib, os


class Email:
    def __init__(self):
        self.message_obj = email.mime.multipart.MIMEMultipart
        self.smptlib = smtplib
        self.sender = 'no-reply@ucsd.edu'

    def send_html(self, receiver, subject, html_message):
        message = self.message_obj('alternative')
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = receiver
        
        html = email.mime.text.MIMEText(html_message, 'html')
        message.attach(html)
        
        with self.smptlib.SMTP_SSL(os.environ['SMTP_SERVER']) as server:
            server.sendmail(self.sender, receiver, message.as_string())
            server.quit()

# def send_email(sender, receiver, msg):
#     message = email.mime.multipart.MIMEMultipart('alternative')
#     message['Subject'] = 'Your account is out of disk space'
#     message['From'] = 'no-reply@ucsd.edu'
#     message['To'] = receiver
    
#     html = email.mime.text.MIMEText(OUT_OF_DISK_SPACE, 'html')
#     message.attach(html)
    
#     with smtplib.SMTP_SSL(os.environ['SMTP_SERVER']) as server:
#         server.sendmail(sender, receiver, msg)
#         server.quit()