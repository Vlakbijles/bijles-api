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


# Main parser used for parsing the default fields (api_user, timestamp, data, hash)
main_parser = reqparse.RequestParser()
main_parser.add_argument('api_user', type=str, required=True, help="api_user required")
main_parser.add_argument('timestamp', type=str, required=True, help="timestamp required")
main_parser.add_argument('data', type=dict, required=True, help="data required")
main_parser.add_argument('hash', type=str, required=True, help="hash required")

data_parser = reqparse.RequestParser()
data_parser.add_argument('user', type=dict, location=('data',))

data_parser = reqparse.RequestParser()
data_parser.add_argument('usermeta', type=dict, location=('data',))

user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, help="email", location('user'))
user_parser.add_argument('password', type=str, help="email", location('user'))

usermeta_parser = reqparse.RequestParser()
usermeta_parser.add_argument('name', type=str, help="email", location('usermeta'))
usermeta_parser.add_argument('surname', type=str, help="surname", location('usermeta'))
usermeta_parser.add_argument('postal_code', type=str, help="postal_code", location('usermeta'))
usermeta_parser.add_argument('phone', type=str, help="phone", location('usermeta'))
usermeta_parser.add_argument('photo_id', type=str, help="photo_id", location('usermeta'))
usermeta_parser.add_argument('facebook_token', type=str, help="facebook_token", location('usermeta'))
usermeta_parser.add_argument('description', type=str, help="description", location('usermeta'))


class UserResource(Resource):

    def __init__(self):
        pass

    @marshal_with(user_fields)
    # delete is used for giving info about a user model
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user, 201

    # delete is used for deleting a user model
    # TODO: Add verification
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    @marshal_with(user_fields)
    # put is used for updating a user model
    # TODO: Add verification
    def put(self, id):
        args = main_parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))

        user_args = self.user_parser.parse_args(args['data']['user'])
        # if user exists, see which data is sent and change user accordingly
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.password = args['password']
        session.add(user)
        session.commit()
        return user, 201


class UserCreationResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

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
    'offers': fields.List(fields.Nested(offer_fields)),
}


class UserOfferResource(Resource):

    def __init__(self):
        self.data_parser = reqparse.RequestParser()
        self.data_parser.add_argument('offer', type=dict, required=True, location=('data'))

        self.offer_parser = reqparse.RequestParser()
        self.offer_parser.add_argument('subject_id', type=str, required=True, location=('offer',))
        self.offer_parser.add_argument('level_id', type=str, required=True, location=('offer',))

    @marshal_with(offer_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        return user.offers

    @marshal_with(offer_fields)
    # TODO: Add verification
    def post(self, id):
        args = main_parser.parse_args()
        user = session.query(User).filter(User.id == id).first()

        data_args = self.data_parser.parse_args(req=args)
        offer_args = self.offer_parser.parse_args(req=data_args)

        user.offers.append(Offer(subject_id=offer_args['subject_id'],
                                 level_id=offer_args['level_id']))
        session.add(user)
        session.commit()
        return user, 201
