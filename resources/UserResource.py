#!/usr/bin/env python
"""
UserResource.py, for actions on the User model,
this file is a module and has no use as stand-alone file

UserResource contains the following classes:
- UserByIdResource, acts on the User model based on the User id
- UserResource, for creating a new User model and modifying the logged in User model

"""


from resources import *  # NOQA
from models import User, UserMeta, Postcode


user_fields = {
    'id': fields.Integer,
    'meta.name': fields.String,
    'meta.surname': fields.String,
    'meta.photo_id': fields.String,
    'meta.facebook_token': fields.String,
    'meta.description': fields.String,
}

meta_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'subject_id': fields.Integer,
    'level_id': fields.Integer,
}


# User Data field parser
# Used for parsing the user and user meta fields inside the data field
user_data_parser = reqparse.RequestParser()
user_data_parser.add_argument('user', type=dict, required=True, location=('data'))
user_data_parser.add_argument('meta', type=dict, required=True, location=('data'))

# User parser
# Used for parsing the fields inside the user field
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="email", location=('user'))
user_parser.add_argument('password', type=str, required=True, help="password", location=('user'))

# Usermeta parser
# Used for parsing the fields inside the user meta field
usermeta_parser = reqparse.RequestParser()
usermeta_parser.add_argument('name', type=str, required=True, help="email", location=('usermeta'))
usermeta_parser.add_argument('surname', type=str, required=True, help="surname", location=('usermeta'))
usermeta_parser.add_argument('postcode', type=str, required=True, help="postcode", location=('usermeta'))
usermeta_parser.add_argument('phone', type=str, required=True, help="phone", location=('usermeta'))
usermeta_parser.add_argument('photo_id', type=str, required=True, help="photo_id", location=('usermeta'))
usermeta_parser.add_argument('facebook_token', required=True, type=str, help="facebook_token", location=('usermeta'))
usermeta_parser.add_argument('description', required=True, type=str, help="description", location=('usermeta'))


class UserByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/user/<int:id>"

    GET is used for giving info about an User model, given an User id
    PUT is used for changing info about an User model, given an User id,
        you cannot create a user using this method.
    DELETE is used deleting an User model, given an User id

    """

    def __init__(self):
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        return user, 200

    @api_validation
    @marshal_with(user_fields)
    def put(self, id):
        # Parse from the "user" field and "usermeta" field
        user_data_args = user_data_parser.parse_args(self.args)
        user_data = user_parser.parse_args(user_data_args)
        usermeta_data = usermeta_parser.parse_args(user_data_args)

        # Check if user with id exists
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        if user_data['email']:
            user.email = user_data['email']
        if user_data['password']:
            user.password = user_data['password']
        session.add(user)
        session.commit()

        return usermeta_data, 201

    @api_validation
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        session.delete(user)
        session.commit()
        return {}, 204


class UserResource(Resource):
    """
    Class for handling the GET, POST requests for "/user"

    GET not yet implemented, is used for managing the logged in User model
    POST is used for creating an new User model

    """

    def __init__(self):
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @marshal_with(user_fields)
    # TODO: not yet implemented
    def get(self):
        pass

    @api_validation
    @marshal_with(user_fields)
    def post(self):
        user_data = self.args['data']['user']
        usermeta_data = self.args['data']['usermeta']

        user = User(email=user_data['email'], password=user_data['password'])
        postcode = session.query(Postcode).filter(Postcode.postcode == usermeta_data['postcode']).first()
        if not user:
            abort(400, message="Postcode ({}) not found".format(usermeta_data['postcode']))


        user.meta = UserMeta(name=usermeta_data['name'],
                             surname=usermeta_data['surname'],
                             postcode=usermeta_data['postcode'],
                             latitude=postcode.lat,
                             longitude=postcode.lon,
                             phone=usermeta_data['phone'],
                             photo_id='photo',
                             facebook_token='fb_token',
                             description=usermeta_data['desc'])
        session.add(user)
        session.commit()
        return user, 201
