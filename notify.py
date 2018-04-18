import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess as s
import sys
import os

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
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def push_notification(predicted_change, sentiment, coin):
    message = coin + "\n" + \
    "Sentiment : " + sentiment + "\n" + \
    "Predicted Change :" + predicted_change
    if sys.platform.startswith("linux"):
        s.call(['notify-send', message])
    else: # Mac
        os.system("""
        osascript -e 'display notification"{}" with title "{}" subtitle "{}"'
                """.format("Sentiment : " + sentiment,coin, "Predicted Change :" + predicted_change))

def push_notification_details(flag):
    if flag:
        if sys.platform.startswith("linux"):
            message = "Your details have been updated."
            s.call(['notify-send', message])
        else: #Mac
            os.system("""
                        osascript -e 'display notification"{}" with title "{}"'
            """.format("Your details have been updated.", "Successful"))
    else:
        if sys.platform.startswith("linux"):
            message = "Your details have not been updated. Enter an email."
            s.call(['notify-send', message])
        else: #Mac
            os.system("""
                        osascript -e 'display notification"{}" with title "{}"'
            """.format("Your details have not been updated. Enter an email.", "Unsuccessful"))
