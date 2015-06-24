import smtplib

SERVER = "localhost"

FROM = "noreply@vlakbijles.nl"

SUBJECT = "Vlakbijles Gebuiker heeft je een bericht gestuurd over vak"
TEXT = "This message was sent with Python's smtplib."


def email(subject, text, recipient):
    # Message template, insert actual data
    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(recipient), subject, text)

    try:
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, recipient, message)
        print("Successfully sent email")
    except:
        print("Error: unable to send email")


if __name__ == '__main__':
    email(SUBJECT, TEXT, "gmverkes@gmail.com")
