Vlakbijles API
===================
Requirements:
    - flask
    - flask-restful
    - sqlalchemy

Formatting requests
-------------------
Every API client has a unique alphanumerical username and a private 128-bit key
(represented as a string in hexadecimal) known to the API client and server.
API requests are (mostly) RESTful HTTP requests validated using HMAC (with
SHA256 encryption).

First set up the following JSON object (all values **_must_** be strings):
```javascript
{
    "api_user": "your_api_username",
    "data": {
			     ..
			},
    "timestamp": "current_utc_timestamp"
}
```
Fill the `data`  with the necessary values if applicable, if the requests does
not need to send over data it can be left empty (that is `"data": {}`). What
follows is an example (in Python) demonstrating which values and in what order
they should be used to calculate the hash:

```python
import hmac
import json
from hashlib import sha256

api_key = "abcdefghijklmnopqrstuvwxyz123456"
uri = "/example/1" # Requested path in full, including possible query string
method = "POST"
request = {
              "api_user": "example_api_user",
              "data": {
	                      "b_example": {
		                                  "c": "example3",
                                          "b": "example2",
                                          "a": "example1"
                                      },
                          "a_example": {
                                          "f": "example6",
                                          "e": "example5",
                                          "d": "example4"
                                      }
                      },
              "timestamp": "1234567890"
}

# Convert request to a flattened compact JSON string for use in hash
# calculation, conversion removes whitespace/newlines and sorts all entries
# alphabetically by key
request_formatted = json.dumps(request, sort_keys=True, separators=(",", ":"))

# Calculate hash
hash = hmac.new(api_key, request_formatted, sha256)
hash.update(uri + method) # Equivalent to hash.update(uri); hash.update(method)

# Append hash to original request (represented as a hexadecimal string)
request["hash"] = hash.hexdigest()
```

The method of conversion of `request` to `request_formatted` **_must_** be
adhered to in order for the server to validate the API request. For the example
above, the resulting string used in the hash calculation looks like this:

```
{"api_user":"example_api_user","data":{"example1":{"a":"example1","b":"example2","c":"example3"},"example2":{"d":"example4","e":"example5","f":"example6"}},"timestamp":"1234567890"}
```

Note that the final JSON object should include the calculated hash in the
`"hash"` field, while JSON object used in the hash calculation itself does not.
The final JSON string in the HTTP request body does _not_ need to be formatted
a described above, it is only required for the hash calculation.

Example request:

```
POST /example/1 HTTP/1.1
Host: www.example.com
Content-type: application/json

{
	"api_user": "example_api_user",
    "data": {
		        "b_example": {
                                 "c": "example3",
                                 "b": "example2",
                                 "a": "example1"
                             },
                "a_example": {
                                 "f": "example6",
                                 "e": "example5",
                                 "d": "example4"
                             }
             },
	"timestamp": "1234567890",
	"hash": "d38f3c7bbdc45342cd29627aa145fd0c2a5196e47f5419c870ba8eace06b1a5a"
}
```

Available requests
-------------------
Creating users:

|METHOD   |`/user`|SUCCESS|ERROR|
|---------|-------|-------|-----|
|`POST`   |data:userdata|`201`|`400`|

Retrieving/updating user data, removing users:

|METHOD   |`/user/user_id`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`GET`    |data:-|`200`|`404`|
|`PUT`    |data:token,iets|`200`|`400`, `401`, `404`|
|`DELETE` |data:token,password|`200`|`400`, `401`, `404`|

Retrieving/creating user offers:

|METHOD   |`/user/user_id/offer`|SUCCESS|ERROR|
|---------|---------------------|-------|-----|
|`GET`    |data:-|`200`|`404`|
|`POST`   |data:token,iets|`201`|`400`, `401`|

Retrieving list of reviews of user:

|METHOD   |`/user/user_id/review`|SUCCESS|ERROR|
|---------|----------------------|-------|-----|
|`GET`    |data:-|`200`|`404`|

Retrieving/creating/updating/removing user reviews:

|METHOD   |`/review/offer_id`|SUCCESS|ERROR|
|---------|------------------|-------|-----|
|`GET`    |data:-|`200`|`404`|
|`POST`   |data:token,reviewdata|`201`|`400`, `401`|
|`PUT`    |data:token,reviewdata|`200`|`400`, `401`, `404`|
|`DELETE` |data:token|`200`|`401`, `404`|

Retrieving offers:

|METHOD   |`/offers?subject_id=<int:subject_id>&postal_code=<str:postal_code>&level_id=<int:level_id>&page=<int:page number>&order_by<distance, no_reviews, no_endorsed>`|SUCCESS|ERROR|
|---------|-------------------------------------------------------|-------|-----|
|`GET`    |loc:, range:, subject_id:, level:, sortby:|`200`|`204`, `400`|



```
/user?
```

GET
```
{
	"api_user": "<api user>",
    "data": {
                "loggedin_data": {
                                    "user_id":    "<user id>",
                                    "token_hash": "<user token hash>"
                                 }
            },
	"timestamp": "<timestamp>",
	"hash": "<hash>"
}
```

POST
```
{
	"api_user": "<api user>",
    "data": {
		        "user_data":     {
                                   "email":   "<user email>"
                                 },
                "user_meta_data": {
                                   "zipcode": "<user zipcode>",
                                   "fb_id":   "<user facebook token>",
                                 }
            },
	"timestamp": "<timestamp>",
	"hash": "<hash>"
}
```

PUT
```
{
	"api_user": "<api user>",
    "data": {
		        "user_data":     {
                                   "email":   "<user email>"
                                 },
                "user_meta_data": {
                                   "phone":       "<user phone>",
                                   "zipcode":     "<user zipcode>",
                                   "description": "<user description>"
                                 }
            },
	"timestamp": "<timestamp>",
	"hash": "<hash>"
}
```

```
/user/<user_id>?
```
GET
