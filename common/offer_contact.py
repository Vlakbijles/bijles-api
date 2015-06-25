import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER = "localhost"

FROM = "noreply@vlakbijles.nl"

SUBJECT = "Vlakbijles Gebuiker heeft je een bericht gestuurd over vak"
TEXT = "This message was sent with Python's smtplib."


def offer_contact(subject, text, recipient, sender):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['Reply-To'] = sender
    msg['To'] = recipient

    text = "Beste %s, \n%s heeft je het volgende bericht gestuurd. \n\n%s" %\
           (recipient, sender, text)
    html = """\
    <html>
      <head></head>
      <body>
        <p>
            Beste %s,</br>%s heeft je het volgende bericht gestuurd.</br></br>%s
        </p>
      </body>
    </html>
    """ % (recipient, sender, text)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    try:
        # Send the message via local SMTP server.
        s = smtplib.SMTP('localhost')
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(FROM, recipient, msg.as_string())
        s.quit()
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
