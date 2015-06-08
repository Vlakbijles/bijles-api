Vlakbijles API
===================

Requirements:
    - flask
    - flask-restful
    - sqlalchemy

# API Protocol

Every API client has a alphanumerical username and a private 128-bit key. All
API requests are verified using a HMAC hash, calculated as follows (example in
Python):

```
import hmac
from hashlib import
hash = hmac.new(private_key, utc_timestamp, sha256)
hash.update(http_uri)                               # HTTP request URI as string
hash.update(http_method)                            # HTTP method as string

# Data alphabetically sorted by key
for entry in data:
    hash.update(entry)
```

**Note: utc_timesmap in hash calculation must be identical to the one in the JSON data**

JSON data template:

```
{
    "api_user": api_user,
    "data" = {
               ..
             },
    "hash": hash,
    "timestamp": utc_timestamp
}
```

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

|METHOD   |`/offer?loc=X&range=X&subject_id=X&level=X&p=&sortby=X`|SUCCESS|ERROR|
|---------|-------------------------------------------------------|-------|-----|
|`GET`    |loc:, range:, subject_id:, level:, sortby:|`200`|`204`, `400`|

Example:
```
asd
```
