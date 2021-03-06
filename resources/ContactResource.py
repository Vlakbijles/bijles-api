#!/usr/bin/env python
"""
    ContactResource.py, for actions
    this file is a module and has no use as stand-alone file

    UserResource contains the following classes:
    - UserByIdResource, acts on the User model based on the User id
    - UserResource, for creating a new User model and modifying the logged in User model

"""


from resources import *  # NOQA
from models import User, Offer
from common.offer_contact import offer_contact


class ContactResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/contact/<int:offer_id>"

    GET is used for giving info about a User model, given a User id
    PUT is used for changing info about a User model, given a User id,
        you cannot create a user using this method.
    DELETE is used deleting a User model, given a User id

    """

    @api_validation
    @authentication(None)
    def post(self, offer_id):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))
        offer_contact_data = offer_contact_parser.parse_args(data_parser("contact"))

        offer = session.query(Offer).filter(Offer.id == offer_id).first()
        user_recipient = session.query(User).filter(User.id == offer.user_id).first()
        if not user_recipient:
            abort(400, message="Recipient User with id={} doesn't exist".format(user_recipient.id))

        user_sender = session.query(User).filter(User.id == loggedin_data["user_id"]).first()
        if not user_sender:
            abort(400, message="Sender User with id={} doesn't exist".format(loggedin_data["user_id"]))

        subject = "{} heeft gereageerd op je vak aanbieding: {}.".format(user_sender.meta.name, offer.subject.name)
        message = "Beste {},<br><br>{} heeft gereageerd op uw {} bijles aanbieding met het volgende bericht:<br><br>\"{}\"<br><br>U kunt contact opnemen met {} door te antwoorden op deze email, of door rechtstreeks een email te sturen naar het volgende adres:<br><br>{}<br><br>Met vriendelijke groet,<br>Het Vlakbijles team".format(user_recipient.meta.name, user_sender.meta.name, offer.subject.name, offer_contact_data["message"], user_sender.meta.name, user_sender.email)
        offer_contact(subject, message, user_recipient.email, user_sender.email)

        return {}, 200
