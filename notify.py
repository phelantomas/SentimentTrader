import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess as s

def send_email(predicted_change, sentiment, coin, toaddr):
    fromaddr = "cryptocurrency.sentiment@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Predicted Price Change Of " + coin

    body = "The sentiment of the last 60 minutes for " + coin + " is : " + sentiment + \
           " - The predicted change in price is : " + predicted_change
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

def push_notification(predicted_change, sentiment, coin):
    message = coin + "\n" + \
    "Sentiment : " + sentiment + "\n" + \
    "Predicted Change :" + predicted_change
    s.call(['notify-send', message])

def push_notification_details():
    message = "Your details have been updated."
    s.call(['notify-send', message])