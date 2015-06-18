#!/usr/bin/env python
"""
    UserResource.py, for actions on the User model,
    this file is a module and has no use as stand-alone file

    UserResource contains the following classes:
    - UserByIdResource, acts on the User model based on the User id
    - UserResource, for creating a new User model and modifying the logged in User model

"""


from resources import *  # NOQA
from models import User, UserMeta, Zipcode


offer_fields = {
    'id': fields.Integer,
    'subject.name': fields.String,
    'level.name': fields.String,
    'review.rating': fields.Integer,
    'review.description': fields.String
}

user_fields = {
    'id': fields.Integer,
    'meta.name': fields.String,
    'meta.surname': fields.String,
    'meta.age': fields.Integer,
    'meta.zipcode': fields.String,
    'meta.city': fields.String,
    'meta.photo_id': fields.String,
    'meta.description': fields.String,
    # 'offers': fields.List(fields.Nested(offer_fields)),
}


class UserByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/user/<int:id>"

    GET is used for giving info about a User model, given a User id
    PUT is used for changing info about a User model, given a User id,
        you cannot create a user using this method.
    DELETE is used deleting a User model, given a User id

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

    # TODO: ONLY FOR ADMIN
    # @api_validation
    # @marshal_with(user_fields)
    # def put(self, id):
    #     # Parse from the "user" field and "usermeta" field
    #     user_data_args = user_data_parser.parse_args(self.args)
    #     user_data = user_parser.parse_args(user_data_args)
    #     usermeta_data = usermeta_parser.parse_args(user_data_args)
    #
    #     # Check if user with id exists
    #     user = session.query(User).filter(User.id == id).first()
    #     if not user:
    #         abort(404, message="User with id={} doesn't exist".format(id))
    #
    #     if user_data['email']:
    #         user.email = user_data['email']
    #     if user_data['password']:
    #         user.password = user_data['password']
    #     session.add(user)
    #     session.commit()
    #
    #     return usermeta_data, 201
    #
    # @api_validation
    # def delete(self, id):
    #     user = session.query(User).filter(User.id == id).first()
    #     if not user:
    #         abort(404, message="User with id={} doesn't exist".format(id))
    #
    #     session.delete(user)
    #     session.commit()
    #     return {}, 204


class UserResource(Resource):
    """
    Class for handling the GET, POST requests for "/user"

    GET is used for showing the logged in User model
    PUT is used for modifying the logged in User model
    GET is used for modifying the logged in User model
    POST is used for creating a new User model

    """

    def __init__(self):
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @authentication(None)
    @marshal_with(user_fields)
    def get(self):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin", self.args))

        user = session.query(User).filter(User.id == loggedin_data['user_id']).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        return user, 200

    @api_validation
    @authentication(None)
    @marshal_with(user_fields)
    def put(self):
        pass

    @api_validation
    @marshal_with(user_fields)
    def post(self):
        user_data = user_parser.parse_args(data_parser("user", self.args))
        usermeta_data = usermeta_parser.parse_args(data_parser("usermeta", self.args))

        # Check if email is already used for another user
        user = session.query(User).filter(User.email == user_data['email']).first()
        if user:
            abort(400, message="Email ({}) is already in use".format(user_date['email']))

        # Check if zipcode is valid
        zipcode = session.query(Zipcode).filter(Zipcode.zipcode == usermeta_data['zipcode']).first()
        if not zipcode:
            abort(400, message="Zipcode ({}) not found".format(usermeta_data['zipcode']))

        user = User(email=user_data['email'])

        fb_data = get_fb_user_data(usermeta_data['fb_token'])

        # Check if the facebook token matches with real account
        if not fb_data:
            abort(400, message="Link to Facebook account failed")

        user.meta = UserMeta(name=fb_data['name'],
                             surname=fb_data['surname'],
                             zipcode=zipcode.zipcode,
                             latitude=zipcode.lat,
                             longitude=zipcode.lon,
                             city=zipcode.city,
                             photo_id=fb_data['picture'],
                             facebook_id=fb_data['id'])

        session.add(user)
        session.commit()

        return user, 201
