"""
    args_parser.py, this file contains all arguments parser

"""


from flask.ext.restful import inputs
from flask.ext.restful import reqparse

# Main parser
# Used for parsing the default json data fields (api_user, timestamp, data, hash)
main_parser = reqparse.RequestParser()
main_parser.add_argument('api_user', type=str, required=True, help="api_user")
main_parser.add_argument('timestamp', type=str, required=True, help="timestamp")
main_parser.add_argument('data', type=dict, required=True, help="data")
main_parser.add_argument('hash', type=str, required=True, help="hash")


def data_parser(field):
    args = main_parser.parse_args()
    data_parser = reqparse.RequestParser()
    data_parser.add_argument(field, type=dict, required=True, help=field, location=('data'))
    return data_parser.parse_args(args)


# Used for parsing the fields inside the user field
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="email", location=('user'))


# Used for parsing the fields inside the usermeta field
usermeta_parser = reqparse.RequestParser()
usermeta_parser.add_argument('zipcode', required=True, type=inputs.regex("[0-9]{4}[A-Za-z]{2}"), help="zipcode", location=('usermeta'))
usermeta_parser.add_argument('fb_token', required=True, type=str, help="fb_token", location=('usermeta'))
usermeta_parser.add_argument('phone', type=str, help="phone", location=('usermeta'))
usermeta_parser.add_argument('description', type=str, help="description", location=('usermeta'))


# Used for parsing the fields inside the loggedin field
loggedin_parser = reqparse.RequestParser()
loggedin_parser.add_argument('user_id', type=int, required=True, help="user_id", location=('loggedin'))
loggedin_parser.add_argument('token_hash', type=str, required=True, help="token_hash", location=('loggedin'))

# Used for parsing the facebook access token the facebook field
fb_access_token_parser = reqparse.RequestParser()
fb_access_token_parser.add_argument('access_token', type=str, required=True, help="access_token", location=('facebook'))


# Offer parser used for parsing the fields inside offer field
offer_parser = reqparse.RequestParser()
offer_parser.add_argument('subject_id', type=str, required=True, location=('offer'))
offer_parser.add_argument('level_id', type=str, required=True, location=('offer'))
offer_parser.add_argument('active', type=str, required=True, location=('offer'))


# Offer Search parser used for parsing the search query arguments
offersearch_parser = reqparse.RequestParser()
offersearch_parser.add_argument('loc', type=str, required=True, location=('args'))
offersearch_parser.add_argument('range', type=int, required=True, location=('args',))
offersearch_parser.add_argument('subject', type=int, required=True, location=('args'))
offersearch_parser.add_argument('level', type=int, required=True, location=('args'))
offersearch_parser.add_argument('page', type=int, required=True, location=('args'))
offersearch_parser.add_argument('sortby', type=str, required=True, location=('args'))