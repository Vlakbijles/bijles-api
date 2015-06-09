# User Resource, for actions on the Offer model which is related to the User model

from resources import reqparse
from resources import abort
from resources import Resource
from resources import fields
from resources import marshal_with

from resources.models import User, Offer
from resources.db import session
from resources import main_parser


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
        # Used for parsing the user and usermeta fields inside the data field
        self.user_data_parser = reqparse.RequestParser()
        self.user_data_parser.add_argument('offer', type=dict, required=True, location=('data'))

        # Usermeta parser
        # Used for parsing the fields inside the usermeta field
        self.offer_parser = reqparse.RequestParser()
        self.offer_parser.add_argument('subject_id', type=str, required=True, location=('offer',))
        self.offer_parser.add_argument('level_id', type=str, required=True, location=('offer',))

    @marshal_with(offer_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        # for offer in user.offers:
        #     user.offersk offer.subject.name
        #     print offer.level.name
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


class OfferByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/offer/<int:id>"

    GET is used for receiving all offers linked to the User model, given the User id
    POST is used for creating a new offer linked to the User model, given the User id
    DELETE TODO: not yet implemented

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
