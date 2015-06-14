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
lat = 52.6759082590322
lon = 4.7038764017095
# uri = "/offer?loc={lat},{lon}&range=10000&subject=200&level=2&page=2&sortby=apj".format(lat=lat, lon=lon)
# uri = "/user/1?"
uri = "/user?"
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
            "token_hash": "621aabbdb6f36802c79eae7d0436abbfaa2dfb4de2285f114cf44816cd9e44b2",
        },
        #
        # "usermeta": {
        #     "name": "asdjq",
        #     "surname": "asdpwq",
        #     "postcode": "1078MJ",
        #     "phone": "asdqp23r",
        #     "desc": "posadwu",
        # }
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
