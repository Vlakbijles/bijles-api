from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import request
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

from common.db import session
from common.authentication import api_validation


__all__ = ['reqparse', 'request', 'abort', 'Resource', 'fields', 'marshal_with', 'session',
           'main_parser', 'api_validation']

# Main parser
# Used for parsing the default json data fields (api_user, timestamp, data, hash)
main_parser = reqparse.RequestParser()
main_parser.add_argument('api_user', type=str, required=True, help="api_user")
main_parser.add_argument('timestamp', type=str, required=True, help="timestamp")
main_parser.add_argument('data', type=dict, required=True, help="data")
main_parser.add_argument('hash', type=str, required=True, help="hash")
