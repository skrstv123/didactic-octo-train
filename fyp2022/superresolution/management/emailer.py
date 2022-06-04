# method to send email with attachment using python:
import smtplib  
from django.conf import settings
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def serversetup():
    print("Setting up server...",
    f"using sender: {settings.EMAIL_HOST} and email: {settings.EMAIL_SENDER}",
    sep="\n")
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.connect(settings.EMAIL_HOST,settings.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
    return server

def send_email(message_dict):
    print("Sending email...",
    f"using sender: {settings.EMAIL_HOST} and email: {settings.EMAIL_SENDER}",
    sep="\n")
    server = serversetup()
    message = MIMEMultipart()

    message['From'] = settings.EMAIL_SENDER
    message['To'] = message_dict['to']
    message['Subject'] = message_dict['subject']

    message.attach(MIMEText(message_dict['message']))
    
    part = MIMEApplication(message_dict['file'], Name=message_dict['file_name'])
    part['Content-Disposition'] = f'attachment; filename="{message_dict["file_name"]}"'
    message.attach(part)
    server.sendmail(settings.EMAIL_SENDER, message_dict['to'], message.as_string())
    server.quit()
    print("Email sent!")

