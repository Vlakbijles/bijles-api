#!/usr/bin/env python
"""
OfferResource.py, for actions on the Offer model which is related to the User model.
this file is a module and has no use as stand-alone file

Offer Resouces contains the following classes:
- OfferByUserIdResource, acts on Offers based on the User id
- OfferResource, acts on all Offers (e.g. searching)
- OfferByIdResource, acts on a Offer based on the Offer id

"""


from resources import *  # NOQA
from common.helper import latlon_distance
from models import User, Offer


offer_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'level.name': fields.String,
    'subject.name': fields.String,
}


class OfferByUserIdResource(Resource):
    """
    Class for handling the GET and PUT requests for "/user/<int:id>/offer",
    which acts on offer based on their corresponding User id

    GET is used for receiving all offers linked to the User model given the User id
    POST is used for creating a new offer linked to the User model given the User id

    """

    def __init__(self):
        # Parse all class-wide used data
        self.method = request.method
        self.path = request.full_path
        self.args = main_parser.parse_args()

        # User Data field parser
        # Used for parsing the user and user meta fields inside the data field
        self.user_data_parser = reqparse.RequestParser()
        self.user_data_parser.add_argument('offer', type=dict, required=True, location=('data'))

        # Usermeta parser
        # Used for parsing the fields inside the user meta field
        self.offer_parser = reqparse.RequestParser()
        self.offer_parser.add_argument('subject_id', type=str, required=True, location=('offer',))
        self.offer_parser.add_argument('level_id', type=str, required=True, location=('offer',))

    @api_validation
    @marshal_with(offer_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        return user.offers, 200

    @api_validation
    @marshal_with(offer_fields)
    def post(self, id):
        data_args = self.data_parser.parse_args(self.args)
        offer_args = self.offer_parser.parse_args(data_args)

        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        user.offers.append(Offer(subject_id=offer_args['subject_id'],
                                 level_id=offer_args['level_id']))
        session.add(user)
        session.commit()
        return user, 201


class OfferResource(Resource):
    """
    Class for handling the GET requests for "/offer?query"

    GET is used for receiving all offers given a searching specification,
        the search specification are:
            - Location, latitude and longitude given in degrees
            - Range around location, allowed distance to location in meters
            - Subject, id of the subject
            - Level, id of the level
            - Sorting by, spicifies the criteria to sort on

    """

    def __init__(self):
        # Parse all class-wide used data
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

        # Offer Search parser
        # Used for parsing the search query arguments
        self.offer_args_parser = reqparse.RequestParser()
        self.offer_args_parser.add_argument('loc', type=str, required=True, location=('args'))
        self.offer_args_parser.add_argument('range', type=int, required=True, location=('args',))
        self.offer_args_parser.add_argument('subject', type=int, required=True, location=('args'))
        self.offer_args_parser.add_argument('level', type=int, required=True, location=('args'))
        self.offer_args_parser.add_argument('page', type=int, required=True, location=('args'))
        self.offer_args_parser.add_argument('sortby', type=str, required=True, location=('args'))

    @api_validation
    @marshal_with(offer_fields)
    def get(self):
        args = self.offer_args_parser.parse_args()
        offers = session.query(Offer).filter(Offer.subject_id == args['subject'],
                                             Offer.level_id == args['level']).all()

        loc_lat, loc_lon = map(float, args['loc'].split(','))

        result_offers = []

        for offer in offers:
            offer_lat = float(offer.user.meta.latitude)
            offer_lon = float(offer.user.meta.longitude)
            if latlon_distance(loc_lat, loc_lon, offer_lat, offer_lon) < args['range']:
                result_offers.append(offer)

        if not result_offers:
            abort(404, message="No offers found")

        return result_offers, 200


class OfferByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/offer/<int:id>",
    acts on offers based on the Offer id

    DELETE is used for deleting a offer given the offer id. Verificaion is used
           to permit only deleting offers when they are yours

    """

    def __init__(self):
        # Parse all class-wide used data
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @marshal_with(offer_fields)
    def delete(self, id):
        offer = session.query(Offer).filter(Offer.id == id).first()
        if not offer:
            abort(404, message="Offer with id={} doesn't exist".format(id))

        session.delete(offer)
        session.commit()
        return {}, 201
