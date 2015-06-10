# authentication.py
# Function for validating API requests, to be used as a decorator function

import hmac
import json
import time
import datetime

from functools import wraps
from hashlib import sha256
from config import api_users
from resources import abort


def api_validation(f):
    """
    Regenerates hash from request using the private key associated with
    value in the api_user field, the request JSON data, the full HTTP path
    (including a possible query string) and the HTTP request method.
    Hashes are calculated with the HMAC module (using SHA256 encryption),
    comparison of the hash in the original request to the generated one
    can validate the API request.
    
    """

    @wraps(f)
    def wrapper(*args, **kwargs):

        data_dict = args[0].args
        utc_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))

        # Ignore requests older than 30 seconds
        if utc_now - int(data_dict['timestamp']) < 30:

            if data_dict["api_user"] in api_users:
                api_key = api_users[data_dict["api_user"]]

                # Remove hash field from json data in order to regenerate
                # original hash
                provided_hash = data_dict["hash"]
                del data_dict["hash"]
                data_json = json.dumps(data_dict, sort_keys=True, separators=(",", ":"))

                reconstructed_hash = hmac.new(str(api_key), data_json, sha256)
                reconstructed_hash.update(args[0].full_path)
                reconstructed_hash.update(args[0].method)

                if reconstructed_hash.hexdigest() == provided_hash:
                    return f(*args, **kwargs)

        return abort(401, message="Unauthorized API request")

    return wrapper
