#!/usr/bin/env python
"""
    UserResource.py, for actions on the User model,
    this file is a module and has no use as stand-alone file

    UserResource contains the following classes:
    - UserByIdResource, acts on the User model based on the User id
    - UserResource, for creating a new User model and modifying the logged in User model

"""


from resources import *  # NOQA
from models import User, UserMeta, PostalCode, Review, Offer


offer_fields = {
    'id': fields.Integer,
    'subject.name': fields.String,
    'level.name': fields.String,
    'review.rating': fields.Integer,
    'review.description': fields.String
}

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'meta.name': fields.String,
    'meta.surname': fields.String,
    'meta.age': fields.Integer,
    'meta.postal_code': fields.String,
    'meta.city': fields.String,
    'meta.photo_id': fields.String,
    'meta.description': fields.String,
    'meta.endorsments': fields.Integer,
    'meta.no_reviews': fields.Integer,
}


class UserByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/user/<int:id>"

    GET is used for giving info about a User model, given a User id
    PUT is used for changing info about a User model, given a User id,
        you cannot create a user using this method.
    DELETE is used deleting a User model, given a User id

    """

    @api_validation
    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        # Get average review rating for all user offers, given the user id
        user.meta.no_endorsed = session.query(func.count(Review).label('no_endorsed')). \
            join(Review.offer).filter(Offer.user_id == id, Review.endorsed).first()[0]
        # Get number of reviews for all user offers, given the user id
        user.meta.no_reviews = session.query(func.count(Review).label('no_reviews')). \
            join(Review.offer).filter(Offer.user_id == id).first()[0]

        return user, 200

    # TODO: ONLY FOR ADMIN
    # @api_validation
    # @marshal_with(user_fields)
    # def put(self, id):
    #     # Parse from the "user" field and "user_meta" field
    #     user_data_args = user_data_parser.parse_args(self.args)
    #     user_data = user_parser.parse_args(user_data_args)
    #     user_meta_data = user_meta_parser.parse_args(user_data_args)
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
    #     return user_meta_data, 201
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

    @api_validation
    @authentication(None)
    @marshal_with(user_fields)
    def get(self):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))

        user = session.query(User).filter(User.id == loggedin_data["user_id"]).one()
        if not user:
            abort(204, message="User with id={} doesn't exist".format(id))

        return user, 200

    @api_validation
    @authentication(None)
    @marshal_with(user_fields)
    def put(self):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))
        user_data = user_parser.parse_args(data_parser("user"))
        user_meta_data = user_meta_put_parser.parse_args(data_parser("user_meta"))

        # Get model of the user that is logged in
        user = session.query(User).filter(User.id == loggedin_data["user_id"]).one()

        if (user.email != user_data["email"]):
            # Check if email is already used for another user
            if session.query(User).filter(User.email == user_data['email']).first():
                abort(400, message="Email ({}) is already in use".format(user_data['email']))
            user.email = user_data["email"]

        if (user.meta.postal_code != user_meta_data["postal_code"]):
            # Check if postal_code is valid
            postal_code = session.query(PostalCode).filter(PostalCode.postal_code == user_meta_data['postal_code']).first()
            if not postal_code:
                abort(400, message="PostalCode ({}) not found".format(user_meta_data['postal_code']))
            user.meta.postal_code = postal_code.postal_code
            user.meta.latitude = postal_code.lat
            user.meta.longitude = postal_code.lon
            user.meta.city = postal_code.city

        if (user.meta.description != user_meta_data["description"]):
            if len(user_meta_data["description"]) > 1000:
                abort(400, message="Description exceeded max length of 1000 chars")
            user.meta.description = user_meta_data["description"]

        session.add(user)

        return user, 200

    @api_validation
    @marshal_with(user_fields)
    def post(self):
        user_data = user_parser.parse_args(data_parser("user"))
        user_meta_data = user_meta_parser.parse_args(data_parser("user_meta"))

        # Check if email is already used for another user
        user = session.query(User).filter(User.email == user_data['email']).first()
        if user:
            abort(400, message="Email ({}) is already in use".format(user_data['email']))

        # Check if postal_code is valid
        postal_code = session.query(PostalCode).filter(PostalCode.postal_code == user_meta_data['postal_code']).first()
        if not postal_code:
            abort(400, message="Postal code ({}) not found".format(user_meta_data['postal_code']))

        user = User(email=user_data['email'])

        fb_data = get_fb_user_data(user_meta_data['fb_token'])

        # Check if the facebook token matches with real account
        if not fb_data:
            abort(400, message="Link to Facebook account failed")

        user.meta = UserMeta(name=fb_data['name'],
                             surname=fb_data['surname'],
                             postal_code=postal_code.postal_code,
                             latitude=postal_code.lat,
                             longitude=postal_code.lon,
                             city=postal_code.city,
                             photo_id=fb_data['picture'],
                             facebook_id=fb_data['id'])

        if (user_meta_data['description']):
            user.meta.description = user_meta_data['description']

        session.add(user)

        return user, 201
