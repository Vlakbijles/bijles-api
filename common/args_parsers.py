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

# Used for parsing the fields inside the user_meta field
user_meta_parser = reqparse.RequestParser()
user_meta_parser.add_argument('postal_code', required=True, type=inputs.regex("[0-9]{4}[A-Za-z]{2}"), help="postal_code", location=('user_meta'))
user_meta_parser.add_argument('fb_token', required=True, type=str, help="fb_token", location=('user_meta'))
user_meta_parser.add_argument('description', type=str, help="description", location=('user_meta'))

# Used for parsing the fields inside the user_meta field when updating a users profile
user_meta_put_parser = reqparse.RequestParser()
user_meta_put_parser.add_argument('postal_code', required=True, type=inputs.regex("[0-9]{4}[A-Za-z]{2}"), help="postal_code", location=('user_meta'))
user_meta_put_parser.add_argument('description', type=str, help="description", location=('user_meta'))

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

# Review parser, used for parsing new reviews
review_parser = reqparse.RequestParser()
review_parser.add_argument("offer_id", type=int, required=True, help="offer_id", location=("review"))
review_parser.add_argument("description", type=str, required=False, help="description", location=("review"))
review_parser.add_argument("endorsed", type=bool, required=True, help="endorsed", location=("review"))


# Constants used for offer searching
OFFER_PAGE_SIZE = 8
ORDER_BY_DISTANCE = 'distance'
ORDER_BY_NO_REVIEWS = 'no_reviews'
ORDER_BY_NO_ENDORSED = 'no_endorsed'

# Offer Search parser used for parsing the search query arguments
offersearch_parser = reqparse.RequestParser()
offersearch_parser.add_argument('postal_code', type=inputs.regex("[0-9]{4}[A-Za-z]{2}"), required=True, location=('args'))
offersearch_parser.add_argument('range', type=int, default=50, location=('args'))
offersearch_parser.add_argument('subject_id', type=int, required=True, location=('args'))
offersearch_parser.add_argument('level_id', type=inputs.regex("[0-5]"), default='%', location=('args'))
offersearch_parser.add_argument('page', type=int, required=True, location=('args'))
offersearch_parser.add_argument('order_by', type=str, default=ORDER_BY_DISTANCE, location=('args'),
                                choices=[ORDER_BY_DISTANCE,
                                         ORDER_BY_NO_REVIEWS,
                                         ORDER_BY_NO_ENDORSED])


# Verify Parser is used for parsing the argument to check verify validity
verify_parser = reqparse.RequestParser()
verify_parser.add_argument('verify_type', type=str, required=True, location=('args'))
verify_parser.add_argument('verify_data', type=str, required=True, location=('args'))


# Offer Contact Parser is used for parsing the argument to check verify validity
offer_contact_parser = reqparse.RequestParser()
offer_contact_parser.add_argument('message', type=str, required=True, location=('contact'))
