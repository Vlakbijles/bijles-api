#!/usr/bin/env python2
"""
    authentication.py
    Function for authentication logged in users

"""

import hmac
import time
from hashlib import sha256
from os import urandom
from functools import wraps
from flask.ext.restful import reqparse
from flask.ext.restful import abort

from models import Token
from common.db import session

loggedin_data_parser = reqparse.RequestParser()
loggedin_data_parser.add_argument('loggedin', type=dict, required=True, help="loggedin", location=('data'))

loggedin_parser = reqparse.RequestParser()
loggedin_parser.add_argument('user_id', type=int, required=True, help="user_id", location=('loggedin'))
loggedin_parser.add_argument('token_hash', type=str, required=True, help="token_hash", location=('loggedin'))


# TODO: different types of authentication
def authentication():
    def authentication_inner(f):
        """
        TODO

        """

        @wraps(f)
        def wrapper(*args, **kwargs):

            utc_now = int(time.time())

            loggedin_data_args = loggedin_data_parser.parse_args(args[0].args)
            loggedin_data = loggedin_parser.parse_args(loggedin_data_args)

            # Query for Token with given user id and hash
            token = session.query(Token).filter(Token.user_id == loggedin_data['user_id'],
                                                Token.hash == loggedin_data['token_hash']).first()

            if not token:
                abort(401, message="No match found for given user id and token hash")

            # If token creation date is longer than 7 days ago (604800 seconds) abort
            if (token.create_date + 604800) < utc_now:
                abort(401, message="Token hash expired")
            # If token creation date is longer than 10 minutes ago (600 seconds),
            # refresh creation date to prevent users for loggin out after 7 days (with activity)
            elif (token.create_date + 6000) < utc_now:
                token.create_date = utc_now
                session.add(token)
                session.commit()

            return f(*args, **kwargs)

        return wrapper
    return authentication_inner


def create_token(user_id):
    """
    Generate new token based on user id, time, and random number

    """
    create_date = int(time.time())

    token_hash = hmac.new(str(user_id), str(create_date), sha256)
    token_hash.update(urandom(64))
    token_digest = token_hash.hexdigest()

    return token_digest, create_date
