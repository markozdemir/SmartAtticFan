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
recv_email = "jamesmastran@gmail.com"

def send_fail_email(password, receiver_email, name):

    message = MIMEMultipart("alternative")
    message["Subject"] = "[Alert] Update on Your Attic Fan"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
            Hi """+name+"""!\n
            \n
            We've detected that your attic fan might not be working properly.
            Please go check your attic fan as soon as you can!<
           """
    html = """\
        <html>
            <body>
                <p><b>Hi """+name+"""!</b></p>
                <img src="https://images.cooltext.com/5521216.png" />
                <br />
                <p>We've detected that your attic fan might not be working properly.</p>
                <p>Please go check your attic fan as soon as you can!</p>
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
send_fail_email(password,send_e,name)
