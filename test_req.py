#!/usr/bin/env python2
"""
    test_req.py, used for testing request to the API server
    The private key needs to be added to your *local* config file

"""


import httplib
import json
import hmac
import time

from hashlib import sha256

conn = httplib.HTTPConnection("localhost:5000")

api_user = "test"
private_key = "9103fb5e80d7747ee407505dfa4ca3dc"
loc = "1012BH"
# uri = "/user?"
uri = "/user/1/review?"
# uri = "/offer?loc={loc}&range=1000000&subject=1&level=2&page=2&sortby=apj".format(loc=loc)
method = "GET"
utc_time = str(int(time.time()))


data = {
    "api_user": api_user,
    "timestamp": utc_time,
    "data": {
        "user": {
            "email": "ed@plus.nl",
            "password": "edmin",
        },
        "loggedin": {
            "user_id": 1,
            "token_hash": "4222029021da7403537c00ff01ce8f4068a008333eb28b423e7f5ce68b260db7",
        },
        "offer": {
            "subject_id": 42,
            "level_id": 2,
        },
        "usermeta": {
            "zipcode": "1078MK",
        }
    },
}


# Convert data to alphabetically sorted json string
data_json = json.dumps(data, sort_keys=True, separators=(",", ":"))

# Generate hash
hash = hmac.new(private_key, data_json, sha256)
hash.update(uri)
hash.update(method)

# Append hash
data["hash"] = hash.hexdigest()
data_json = json.dumps(data, sort_keys=True)
headers = {"Content-Type": "application/json"}
conn.request(method, uri, data_json, headers)
res = conn.getresponse()

print(res.status, res.reason)
data = res.read()
print(data)
