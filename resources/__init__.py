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
from flask.ext.restful import marshal
from flask.ext.restful import marshal_with
from sqlalchemy.sql import func

from common.db import get_or_create
from common.db import session
from common.api_validation import api_validation
from common.authentication import authentication, create_token
from common.fbapi import get_fb_user_data
from common.args_parsers import (main_parser, data_parser, user_parser,
                                 user_meta_parser, user_meta_put_parser, offer_parser,
                                 offersearch_parser, loggedin_parser, review_parser,
                                 fb_access_token_parser, verify_parser)


__all__ = ['reqparse', 'request', 'abort', 'Resource', 'fields', 'marshal',
           'marshal_with', 'func', 'session', 'api_validation', 'authentication',
           'create_token', 'main_parser', 'data_parser', 'user_parser', 'review_parser',
           'user_meta_parser', 'user_meta_put_parser', 'offer_parser', 'offersearch_parser',
           'loggedin_parser', 'fb_access_token_parser', 'verify_parser',
           'get_or_create', 'get_fb_user_data']
