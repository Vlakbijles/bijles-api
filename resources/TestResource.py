#!/usr/bin/env python
"""
OfferResource.py, for ac_tions on the Offer model which is related to the User model.
this file is a module and has no use as stand-alone file

Offer Resouces contains the following classes:
- OfferByUserIdResource, acts on Offers based on the User id
- OfferResource, acts on all Offers (e.g. searching)
- OfferByIdResource, acts on a Offer based on the Offer id

"""


from resources import *  # NOQA
from models import User, Offer, PostalCode, Review, Subject, Level

offer_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'user.meta.name': fields.String,
    'user.meta.surname': fields.String,
    'level.name': fields.String,
    'subject.name': fields.String,
    'distance': fields.Integer,
    'user.meta.rating': fields.Float,
    'user.meta.no_reviews': fields.Integer,
}


class TestResource(Resource):
    """
    Class for handling the GET and PUT requests for "/user/<int:id>/offer",
    which acts on offer based on their corresponding User id

    GET is used for receiving all offers linked to the User model given the User id
    POST is used for creating a new offer linked to the User model given the User id

    """

    @marshal_with(offer_fields)
    def get(self):
        offer_data = offer_parser.parse_args(data_parser("offer"))

        print offer_data

        return {}, 200
