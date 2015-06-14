# authentication.py
# Function for authentication logged in users

import time

from functools import wraps
from resources import reqparse
from resources import abort
from resources import session
from models import Token


loggedin_data_parser = reqparse.RequestParser()
loggedin_data_parser.add_argument('loggedin', type=dict, required=True, help="loggedin", location=('data'))

loggedin_parser = reqparse.RequestParser()
loggedin_parser.add_argument('user_id', type=int, required=True, help="user_id", location=('loggedin'))
loggedin_parser.add_argument('token_hash', type=str, required=True, help="token_hash", location=('loggedin'))


# TODO: different types of authentication
def authentication(au_type):
    def authentication_inner(f):
        """
        TODO

        """

        @wraps(f)
        def wrapper(*args, **kwargs):

            utc_now = int(time.time())

            loggedin_data_args = loggedin_data_parser.parse_args(args[0].args)
            loggedin_data = loggedin_parser.parse_args(loggedin_data_args)

            token = session.query(Token).filter(Token.user_id == loggedin_data['user_id'],
                                                Token.hash == loggedin_data['token_hash']).first()

            if not token:
                abort(401, message="No match found for given user id and token hash")
            if token.exp_date < utc_now:
                abort(401, message="Token hash expired")

            return f(*args, **kwargs)

        return wrapper
    return authentication_inner
