#!/usr/bin/env python
"""
    UserResource.py, for actions on the User model,
    this file is a module and has no use as stand-alone file

    UserResource contains the following classes:
    - UserByIdResource, acts on the User model based on the User id
    - UserResource, for creating a new User model and modifying the logged in User model

"""


from resources import *  # NOQA
from models import User, Token
import hmac
import time

from os import urandom
from hashlib import sha256


login_fields = {
    'id': fields.Integer,
    'token': fields.String,
}


# User Data field parser
# Used for parsing the user and user meta fields inside the data field
user_data_parser = reqparse.RequestParser()
user_data_parser.add_argument('user', type=dict, required=True, location=('data'))

# User parser
# Used for parsing the fields inside the user field
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="email", location=('user'))
user_parser.add_argument('password', type=str, required=True, help="password", location=('user'))


class LoginResource(Resource):
    """
    Class for handling the POST requests for "/login"

    POST is used for logging in

    """

    def __init__(self):
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @marshal_with(login_fields)
    @api_validation
    def post(self):
        user_data_args = user_data_parser.parse_args(self.args)
        user_data = user_parser.parse_args(user_data_args)

        user = session.query(User).filter(User.email == user_data['email']).first()
        if not user:
            abort(404, message="User with email={} doesn't exist".format(user_data['email']))
        elif user.password != user_data['password']:
            abort(401, message="Wrong password for email{}".format(user_data['email']))

        token = create_token(user.id)

        return {'id': user.id, 'token': token}, 200


def create_token(user_id):
    """
    Generate new token, add to db

    """
    utc_now = int(time.time())
    expiration_date = utc_now + 604800  # 7 days

    token_hash = hmac.new(str(user_id), str(expiration_date), sha256)
    token_hash.update(urandom(64))
    token_digest = token_hash.hexdigest()

    token = Token(id=user_id, hash=token_digest, exp_date=expiration_date)
    session.add(token)
    session.commit()

    return token_digest


#
#
# class Login(Resource):
#
#     def post(self):
#         if verify_request(request.path, request.method, request.data):
#             # TODO: extract and verify data from post data, perform login, return token
#             return True
