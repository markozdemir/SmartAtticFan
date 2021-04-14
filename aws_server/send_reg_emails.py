from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl;
import smtplib;
import os;
import sys;

sender_email = "thesmartatticfan@gmail.com"

file = open("pw.txt")
password = file.read().replace("\n", "")
file.close()

def send_reg_email(password, receiver_email, name):

    message = MIMEMultipart("alternative")
    message["Subject"] = "[Notification] Registration Was Successful!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
            Hi """+name+"""!\n
            \n
            We are excited to have you on board! Your registration was succesful.\n
            You will receive emails from us from time-to-time if we have to get your attention
            about your attic fan.\n\n
            Best,\n
            The Smart Attic Team
           """
    html = """\
        <html>
            <body>
                <p><b>Hi """+name+"""!</b></p>
                <img src="https://images.cooltext.com/5521216.png" />
                <br />
                <p>We are excited to have you on board! Your registration was succesful.</p.
                <p>You will receive emails from us from time-to-time if we have to get your attention about your attic fan.</p>
                <br />
                <p>Best,</p>
                <p><i>The Smart Attic Team</i></p>
            </body>
        </html>
        """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    # Create secure connection with server and send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

send_e = sys.argv[1]
name = sys.argv[2]
send_reg_email(password,name,send_e)
