import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess as s

def send_email(predicted_change, coin, toaddr):
    print("Starting")
    fromaddr = "cryptocurrency.sentiment@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Predicted Price Change Of " + coin

    body = "The price of " + coin + " will change by " + predicted_change
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP("smtp.gmail.com", "587")
    server.starttls()
    server.ehlo()
    server.login(fromaddr, "Analysis1234")
    text = msg.as_string()
    print(text)
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Over")

def push_notification(predicted_change, coin):
    message = "The predicted change for " + coin + " is " + predicted_change
    s.call(['notify-send', message])