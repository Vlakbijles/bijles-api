#!/usr/bin/env python

import smtplib


def email(sender, contact_offer, contact_msg, recipient):
	sender = "our@email.com"
	receivers = recipient

	headers = """From: our@email.com
	To: %s
	Reply-To: %s
	Content-type = text/html
	Subject: Vlakbijles Gebuiker heeft je een bericht gestuurd over %s
	""" % (recipient, sender, contact_offer)
	body = contact_msg

	message = headers + body

	try:
		server = smtplib.SMTP('vlakbijlessmtphost')
		# server = smtplib.SMTP(smtp.gmail.com, 587)
		# gmail = 'vlakbijles@gmail.com'
		# gmailpassword = 'jsonderulo'
		# smtpObj.login(gmail, gmailpassword)
		server.starttls()
		server.login(onzeemail, password)
		server.sendmail(sender, receivers, message)
		print "Succesfully sent email"
	except
		print "Error: unable to send email"
