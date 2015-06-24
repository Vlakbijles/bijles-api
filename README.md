Vlakbijles API
===================
Required Python modules:
* flask
* flask-restful
* sqlalchemy

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
The final JSON string in the HTTP request body does **_not need_** to be
formatted a described above, it is only required for the hash calculation.

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

### Response codes
* `200` Valid request, either empty or resulting resource is sent back
* `201` Succesfully created resource
* `204` Valid request but no results
* `400` Invalid API request, error message attached

Note: some requests have both `200` and `201` as a response code, if `200` is
returned instead of `201` this means the resource already exists

#### Creating/editing users (POST, PUT), get own profile (GET):

|METHOD   |`/user?`|SUCCESS|ERROR|
|---------|-------|-------|-----|
|`POST`   |data:userdata|`201`|`400`|
|`PUT`    |data:userdata|`200`|`400`|
|`GET`    |data:loggedin|`200`|`400`|

#### Retrieving user profile

|METHOD   |`/user/<int:user_id>?`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`GET`    |data:-|`200`|`404`|

#### Logging in

|METHOD   |`/fblogin?`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`POST`   |data:-|`200`, `202`|-|

#### Email/postal code/subject verification
**IMPORTANT**: returns strings, `"true"` or `"false"`

|METHOD   |`/fblogin?`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`GET`   |Query string: ?verify_type=<str=email, postal_code, subject>&verify_data=<str:data>|`200`|`400`|

Note: email verification returns false if email is already in use, subject
verification is by **id**, _not_ by name

#### Deleting offers

|METHOD   |`/offer/<int:offer_id>?`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`DELETE` |data:loggedin|`200`|`401`, `404`|


#### List of subjects

|METHOD   |`/subject/all?`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`GET`    |data:-|`200`|`204`|


#### List of levels

|METHOD   |`/level/all?`|SUCCESS|ERROR|
|---------|---------------|-------|-----|
|`GET`    |data:-|`200`|`204`|


#### Retrieving a user's offers:

|METHOD   |`/user/<int:user_id>/offer?`|SUCCESS|ERROR|
|---------|---------------------|-------|-----|
|`GET`    |data:-|`200`|`204, 400`|


#### Retrieving the reviews of user identified by id:

|method   |`/user/<int:user_id>/review?`|success|error|
|---------|----------------------|-------|-----|
|`GET`    |data:-|`200`|`400`|


#### Creating a review:

|METHOD   |`/review?`|SUCCESS|ERROR|
|---------|----------------------|-------|-----|
|`POST`   |data:-|`200`, `201`|`400`|


#### Retrieving list of users endorsing a user:

|METHOD   |`/user/<int:user_id>/endorsment?`|SUCCESS|ERROR|
|---------|----------------------|-------|-----|
|`GET`    |data:-|`200`|`400`, `404`|


#### Retrieving/creating/updating/removing user reviews:

|METHOD   |`/review/<int:offer_id>?`|SUCCESS|ERROR|
|---------|------------------|-------|-----|
|`GET`    |data:-|`200`|`404`|
|`POST`   |data:token,reviewdata|`201`|`400`, `401`|
|`PUT`    |data:token,reviewdata|`200`|`400`, `401`, `404`|
|`DELETE` |data:token|`200`|`401`, `404`|


#### Searching for offers (GET), creating offers (POST):

|METHOD   |`/offers?`|SUCCESS|ERROR|
|---------|-------------------------------------------------------|-------|-----|
|`GET`    |Query string: /offers?subject_id=<int:subject_id>&postal_code=<str:postal_code>&level_id=<int:level_id>&page=<int:page_nr>&order_by<str=distance, no_reviews, no_endorsed>|`200`|`204`, `400`|
|`POST`   |data:userdata|`200` `201`|`400`|



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
