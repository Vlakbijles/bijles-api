#!/usr/bin/env python
"""
    FbLoginResource.py, for actions regarding logging in using facebook
    this file is a module and has no use as stand-alone file

    LoginResource contains the following classes:
    - LoginResource, contains POST method for logging in

"""


from resources import *  # NOQA
from models import User, Token, UserMeta


fblogin_fields = {
    'user_id': fields.Integer,
    'token_hash': fields.String,
}

fbregi_fields = {
    'access_token': fields.String,
    'name': fields.String,
    'surname': fields.String,
    'picture': fields.String,
    'email': fields.String,
}


class FbLoginResource(Resource):
    """
    Class for handling the POST requests for "/fblogin?"

    POST is used for logging in as user using facebook

    """

    @api_validation
    def post(self):
        fb = fb_access_token_parser.parse_args(data_parser("facebook", self.args))

        fb_user_data = get_fb_user_data(fb['access_token'])

        user = session.query(User).join(User.meta).filter(UserMeta.facebook_id == fb_user_data['id']).first()

        if not user:
            return marshal(fb_user_data, fbregi_fields), 202

        token_hash, create_date = create_token(user.id)

        token = Token(user_id=user.id, hash=token_hash, create_date=create_date)
        session.add(token)

        return marshal({'user_id': user.id, 'token_hash': token_hash}, fblogin_fields), 200
