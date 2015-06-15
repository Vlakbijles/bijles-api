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
    'offers': fields.List(fields.Nested(offer_fields)),
}


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
    GET is used for modifying the logged in User model
    POST is used for creating an new User model

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
        # Parse from the "user" field and "usermeta" field
        user_data = user_parser.parse_args(data_parser("user", self.args))
        usermeta_data = usermeta_parser.parse_args(data_parser("usermeta", self.args))
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin", self.args))

        # Check if user with id exists
        user = session.query(User).filter(User.id == loggedin_data['user_id']).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        if user_data['email']:
            user.email = user_data['email']
        if user_data['password']:
            user.password = user_data['password']
        if usermeta_data['zipcode']:
            user.meta.zipcode = usermeta_data['zipcode']
        if usermeta_data['phone']:
            user.meta.phone = usermeta_data['phone']
        if usermeta_data['description']:
            user.meta.discription = usermeta_data['discription']
        session.add(user)
        session.commit()

        return user, 200

    @api_validation
    @marshal_with(user_fields)
    def post(self):
        user_data = user_parser.parse_args(data_parser("user", self.args))
        usermeta_data = usermeta_parser.parse_args(data_parser("usermeta", self.args))

        user = User(email=user_data['email'], password=user_data['password'])
        zipcode = session.query(Zipcode).filter(Zipcode.zipcode == usermeta_data['zipcode']).first()
        if not zipcode:
            abort(400, message="Zipcode ({}) not found".format(usermeta_data['zipcode']))

        user.meta = UserMeta(name=usermeta_data['name'],
                             surname=usermeta_data['surname'],
                             age=usermeta_data['data'],
                             zipcode=usermeta_data['zipcode'],
                             latitude=zipcode.lat,
                             longitude=zipcode.lon,
                             city=zipcode.city,
                             phone=usermeta_data['phone'],
                             photo_id='photo',
                             facebook_token='fb_token',
                             description=usermeta_data['desc'])
        session.add(user)
        session.commit()
        return user, 201
