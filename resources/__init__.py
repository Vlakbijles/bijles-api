#!/usr/bin/env python
"""
__init__.py, contain all imports and objects used by all resources

note: when adding an import, add it to the __all__ variable so other modules can use them.

"""

from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import request
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from sqlalchemy.sql import func

from common.db import get_or_create
from common.db import session
from common.api_validation import api_validation
from common.authentication import authentication, create_token
from common.fbapi import get_user_data


__all__ = ['reqparse', 'request', 'abort', 'Resource', 'fields',
           'marshal_with', 'func', 'session', 'api_validation', 'authentication',
           'create_token', 'main_parser', 'data_parser', 'user_parser',
           'usermeta_parser', 'offer_parser', 'offersearch_parser',
           'loggedin_parser', 'get_or_create', 'get_user_data']


# Main parser
# Used for parsing the default json data fields (api_user, timestamp, data, hash)
main_parser = reqparse.RequestParser()
main_parser.add_argument('api_user', type=str, required=True, help="api_user")
main_parser.add_argument('timestamp', type=str, required=True, help="timestamp")
main_parser.add_argument('data', type=dict, required=True, help="data")
main_parser.add_argument('hash', type=str, required=True, help="hash")


def data_parser(field, args):
    data_parser = reqparse.RequestParser()
    data_parser.add_argument(field, type=dict, required=True, help=field, location=('data'))
    return data_parser.parse_args(args)


# Used for parsing the fields inside the user field
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="email", location=('user'))
user_parser.add_argument('password', type=str, required=True, help="password", location=('user'))


# Used for parsing the fields inside the usermeta field
usermeta_parser = reqparse.RequestParser()
usermeta_parser.add_argument('zipcode', type=str, help="zipcode", location=('usermeta'))
usermeta_parser.add_argument('phone', type=str, help="phone", location=('usermeta'))
usermeta_parser.add_argument('description', type=str, help="description", location=('usermeta'))


# Used for parsing the fields inside the loggedin field
loggedin_parser = reqparse.RequestParser()
loggedin_parser.add_argument('user_id', type=int, required=True, help="user_id", location=('loggedin'))
loggedin_parser.add_argument('token_hash', type=str, required=True, help="token_hash", location=('loggedin'))


# Offer parser used for parsing the fields inside offer field
offer_parser = reqparse.RequestParser()
offer_parser.add_argument('subject_id', type=str, required=True, location=('offer'))
offer_parser.add_argument('level_id', type=str, required=True, location=('offer'))


# Offer Search parser used for parsing the search query arguments
offersearch_parser = reqparse.RequestParser()
offersearch_parser.add_argument('loc', type=str, required=True, location=('args'))
offersearch_parser.add_argument('range', type=int, required=True, location=('args',))
offersearch_parser.add_argument('subject', type=int, required=True, location=('args'))
offersearch_parser.add_argument('level', type=int, required=True, location=('args'))
offersearch_parser.add_argument('page', type=int, required=True, location=('args'))
offersearch_parser.add_argument('sortby', type=str, required=True, location=('args'))
