#!/usr/bin/env python2

import httplib
import json
import hmac
import datetime
import time

from hashlib import sha256

conn = httplib.HTTPConnection("127.0.0.1:5000")

api_user = "test"
private_key = "9103fb5e80d7747ee407505dfa4ca3dc"
uri = "/user"
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

                "user_meta": {
                    "name": "asdjq",
                    "surname": "asdpwq",
                    "postal_code": "peqja",
                    "phone": "asdqp23r",
                    "desc": "posadwu",
                }

    }


}

# Convert data to alphabetically sorted json string
data_json = json.dumps(data, sort_keys=True)

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

print hash.hexdigest()


print res.status, res.reason
data = res.read()
print data
