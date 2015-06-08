from models import User, Offer, UserMeta
from db import session

from flask.ext.restful import reqparse
from flask.ext.restful import request
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

# User Resource, for actions on the User model (table)
user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String,
    'verified': fields.Boolean,
    'join_date': fields.DateTime(),
    'last_login': fields.DateTime(dt_format='iso8601'),
}

usermeta_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'subject_id': fields.Integer,
    'level_id': fields.Integer,
}


# Main parser
# Used for parsing the default json data fields (api_user, timestamp, data, hash)
main_parser = reqparse.RequestParser()
main_parser.add_argument('api_user', type=str, required=True, help="api_user")
main_parser.add_argument('timestamp', type=str, required=True, help="timestamp")
main_parser.add_argument('data', type=dict, required=True, help="data")
# main_parser.add_argument('hash', type=str, required=True, help="hash")

# User Data field parser
# Used for parsing the user and usermeta fields inside the data field
user_data_parser = reqparse.RequestParser()
user_data_parser.add_argument('user', type=dict, required=True, location=('data'))
user_data_parser.add_argument('usermeta', type=dict, required=True, location=('data'))

# User parser
# Used for parsing the fields inside the user field
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="email", location=('user'))
user_parser.add_argument('password', type=str, required=True, help="password", location=('user'))

# Usermeta parser
# Used for parsing the fields inside the usermeta field
usermeta_parser = reqparse.RequestParser()
usermeta_parser.add_argument('name', type=str, help="email", location=('usermeta'))
usermeta_parser.add_argument('surname', type=str, help="surname", location=('usermeta'))
usermeta_parser.add_argument('postal_code', type=str, help="postal_code", location=('usermeta'))
usermeta_parser.add_argument('phone', type=str, help="phone", location=('usermeta'))
usermeta_parser.add_argument('photo_id', type=str, help="photo_id", location=('usermeta'))
usermeta_parser.add_argument('facebook_token', type=str, help="facebook_token", location=('usermeta'))
usermeta_parser.add_argument('description', type=str, help="description", location=('usermeta'))


class UserByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/user/<int:id>"

    GET is used for giving info about an User model, given an User id
    PUT is used for changing info about an User model, given an User id,
        you cannot create a user using this method.
    DELETE is used deleting an User model, given an User id

    """

    def __init__(self):
        pass

    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user, 200

    # TODO: Add verification
    @marshal_with(user_fields)
    def put(self, id):
        args = main_parser.parse_args()
        user_data_args = user_data_parser.parse_args(args)

        user_data = user_parser.parse_args(user_data_args)
        usermeta_data = usermeta_parser.parse_args(user_data_args)

        # Check if user with id exists
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))

        if user_data['email']:
            user.email = user_data['email']
        if user_data['password']:
            user.password = user_data['password']
        session.add(user)
        session.commit()

        return usermeta_data, 201

    # TODO: Add verification
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204


class UserResource(Resource):
    """
    Class for handling the GET, POST and DELETE requests for "/user"

    GET TODO: not yet implemented
    POST is used for creating an new User model
    DELETE TODO: not yet implemented

    """

    def __init__(self):
        pass

    @marshal_with(user_fields)
    def post(self):
        args = main_parser.parse_args()
        user_data = args['data']['user']
        user_meta_data = args['data']['user_meta']

        user = User(email=user_data['email'], password=user_data['password'])
        user.meta = UserMeta(name=user_meta_data['name'],
                             surname=user_meta_data['surname'],
                             postal_code=user_meta_data['postal_code'],
                             phone=user_meta_data['phone'],
                             photo_id='photo',
                             facebook_token='fb_token',
                             description=user_meta_data['desc'])
        session.add(user)
        session.commit()
        return user, 201


offer_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'subject_id': fields.Integer,
    'level_id': fields.Integer,
}

user_offers_fields = {
    'offers': fields.List(fields.Nested(offer_fields))
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
        for offer in user.offers:
            print offer.subject.name
            print offer.level.name
        return user.offers, 200

    # TODO: Add verification
    @marshal_with(offer_fields)
    def post(self, id):
        args = main_parser.parse_args()
        data_args = self.data_parser.parse_args(args)
        offer_args = self.offer_parser.parse_args(data_args)

        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))

        user.offers.append(Offer(subject_id=offer_args['subject_id'],
                                 level_id=offer_args['level_id']))
        session.add(user)
        session.commit()
        return user, 201

    # TODO: Add verification
    # def delete(self, id):
    #     user = session.query(User).filter(User.id == id).first()
    #     if not user:
    #         abort(404, message="User {} doesn't exist".format(id))
    #     session.delete(user)
    #     session.commit()
    #     return {}, 204
