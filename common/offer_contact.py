import smtplib

SERVER = "localhost"

FROM = "noreply@vlakbijles.nl"

SUBJECT = "Vlakbijles Gebuiker heeft je een bericht gestuurd over vak"
TEXT = "This message was sent with Python's smtplib."


def offer_contact(subject, text, recipient, sender):
    # Message template, insert actual data
    message = """From: %s
    To: %s
    Reply-To: %s
    Content-type: text/html
    Subject: %s

    %s
    """ % (FROM, recipient, sender, subject, text)

    try:
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, recipient, message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
