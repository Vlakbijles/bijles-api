import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER = "localhost"

FROM = "noreply@vlakbijles.nl"

SUBJECT = "Vlakbijles Gebuiker heeft je een bericht gestuurd over vak"
TEXT = "This message was sent with Python's smtplib."


def offer_contact(subject, text, recipient, sender):
    # Create message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = FROM
    msg['Reply-To'] = sender
    msg['To'] = recipient

    text = "%s" % (text)
    html = """\
    <html>
      <head></head>
      <body>
        <p>
            %s
        </p>
      </body>
    </html>
    """ % (text)

    # Record the MIME types of both parts
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
        s.sendmail(FROM, recipient, msg.as_string())
        s.quit()
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
