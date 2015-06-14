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

from common.db import session
from common.api_validation import api_validation
from common.authentication import authentication, create_token


__all__ = ['reqparse', 'request', 'abort', 'Resource', 'fields', 'marshal_with', 'session',
           'main_parser', 'api_validation', 'authentication', 'create_token',
           'loggedin_data_parser', 'loggedin_parser']

# Main parser
# Used for parsing the default json data fields (api_user, timestamp, data, hash)
main_parser = reqparse.RequestParser()
main_parser.add_argument('api_user', type=str, required=True, help="api_user")
main_parser.add_argument('timestamp', type=str, required=True, help="timestamp")
main_parser.add_argument('data', type=dict, required=True, help="data")
main_parser.add_argument('hash', type=str, required=True, help="hash")

loggedin_data_parser = reqparse.RequestParser()
loggedin_data_parser.add_argument('loggedin', type=dict, required=True, help="loggedin", location=('data'))

loggedin_parser = reqparse.RequestParser()
loggedin_parser.add_argument('user_id', type=int, required=True, help="user_id", location=('loggedin'))
loggedin_parser.add_argument('token_hash', type=str, required=True, help="token_hash", location=('loggedin'))
