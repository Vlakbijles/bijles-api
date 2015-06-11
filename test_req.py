#!/usr/bin/env python2
"""
    test_req.py, used for testing request to the API server
    The private key needs to be added to your *local* config file

"""


import httplib
import json
import hmac
import datetime
import time

from hashlib import sha256

conn = httplib.HTTPConnection("127.0.0.1:5000")

api_user = "test"
private_key = "9103fb5e80d7747ee407505dfa4ca3dc"
lat = 52.6759082590322
lon = 4.7038764017095
# uri = "/offer?loc={lat},{lon}&range=10000&subject=200&level=2&page=2&sortby=apj".format(lat=lat, lon=lon)
uri = "/user?"
method = "POST"
utc_time = str(int(time.mktime(datetime.datetime.utcnow().timetuple())))


data = {
    "api_user": api_user,
    "timestamp": utc_time,
    "data": {
        "user": {
            "email": "tenk",
            "password": "sdads",
        },

        "usermeta": {
            "name": "asdjq",
            "surname": "asdpwq",
            "postcode": "1078MJ",
            "phone": "asdqp23r",
            "desc": "posadwu",
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
