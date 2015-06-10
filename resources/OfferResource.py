# User Resource, for actions on the Offer model which is related to the User model

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
    Class for handling the GET, PUT and DELETE requests for "/user/<int:id>/offer"

    GET is used for receiving all offers linked to the User model, given the User id
    POST is used for creating a new offer linked to the User model, given the User id
    DELETE TODO: not yet implemented

    """

    def __init__(self):
        # User Data field parser
        # Used for parsing the user and user meta fields inside the data field
        self.user_data_parser = reqparse.RequestParser()
        self.user_data_parser.add_argument('offer', type=dict, required=True, location=('data'))

        # Usermeta parser
        # Used for parsing the fields inside the user meta field
        self.offer_parser = reqparse.RequestParser()
        self.offer_parser.add_argument('subject_id', type=str, required=True, location=('offer',))
        self.offer_parser.add_argument('level_id', type=str, required=True, location=('offer',))

    @marshal_with(offer_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        return user.offers, 200

    # TODO: Add verification
    @marshal_with(offer_fields)
    def post(self, id):
        args = main_parser.parse_args()
        data_args = self.data_parser.parse_args(args)
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
            - Location
            - Range around location
            - Subject
            - Level
            - Sorting by

    """

    def __init__(self):
        # Offer Search parser
        # Used for parsing the search query arguments
        self.offer_args_parser = reqparse.RequestParser()
        self.offer_args_parser.add_argument('loc', type=str, required=True, location=('args'))
        self.offer_args_parser.add_argument('range', type=int, required=True, location=('args',))
        self.offer_args_parser.add_argument('subject', type=int, required=True, location=('args'))
        self.offer_args_parser.add_argument('level', type=int, required=True, location=('args'))
        self.offer_args_parser.add_argument('page', type=int, required=True, location=('args'))
        self.offer_args_parser.add_argument('sortby', type=str, required=True, location=('args'))

    @marshal_with(offer_fields)
    def get(self):
        args = self.offer_args_parser.parse_args()
        offers = session.query(Offer).filter(Offer.subject_id == args['subject'],
                                             Offer.level_id == args['level']).all()
        loc_lat, loc_lon = map(int, args['loc'].split(','))
        if not offers:
            abort(404, message="No offers found".format(id))

        for offer in offers:
            offer_lat = offer.user.meta.latitude
            offer_lon = offer.user.meta.longitude
            print(latlon_distance(loc_lat, loc_lon, offer_lat, offer_lon))

        return offers, 200


class OfferByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/offer/<int:id>"

    DELETE is used for deleting a offer given the offer id. Verificaion is used
           to permit only deleting offers when they are yours

    """

    def __init__(self):
        pass

    # TODO: Add verification
    @marshal_with(offer_fields)
    def delete(self, id):
        offer = session.query(Offer).filter(Offer.id == id).first()
        if not offer:
            abort(404, message="Offer with id={} doesn't exist".format(id))

        session.delete(offer)
        session.commit()
        return {}, 201
