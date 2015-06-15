#!/usr/bin/env python
"""
    LoginResource.py, for actions regarding logging in
    this file is a module and has no use as stand-alone file

    LoginResource contains the following classes:
    - LoginResource, contains POST method for logging in

"""


from resources import *  # NOQA
from models import User, Token


login_fields = {
    'user_id': fields.Integer,
    'token_hash': fields.String,
}


class LoginResource(Resource):
    """
    Class for handling the POST requests for "/login"

    POST is used for logging in as user

    """

    def __init__(self):
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @marshal_with(login_fields)
    @api_validation
    def post(self):
        user_data = user_parser.parse_args(data_parser("user", self.args))

        user = session.query(User).filter(User.email == user_data['email']).first()
        if not user:
            abort(404, message="User with email={} doesn't exist".format(user_data['email']))
        elif user.password != user_data['password']:
            abort(401, message="Wrong password for email={}".format(user_data['email']))

        token_hash, create_date = create_token(user.id)

        token = Token(user_id=user.id, hash=token_hash, create_date=create_date)
        session.add(token)
        session.commit()

        return {'user_id': user.id, 'token_hash': token_hash}, 200
