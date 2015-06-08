Vlakbijles API
===================

Requirements:
    - flask
    - flask-restful
    - sqlalchemy

# API Protocol

Every API client has a alphanumerical username and a private 128-bit key. All
API requests are verified using a HMAC hash, calculated using the private key,
timestamp, request URI, HTTP method and data field in the JSON data as follows:

```
hash calculation
```

JSON data template:

```
{
    "api_user": api_user,
    "data" = {
               .. # fields must be alphabetically sorted by key name
             },
    "hash": hash,
    "timestamp": timestamp
}
```

Creating users:

|METHOD   |`/user`|RESPONSES|
|---------|-------|---------|
|`POST`   |data:userdata|Success: `201` Failure: `400`|

Retrieving/updating user data, removing users:

|METHOD   |`/user/user_id`|RESPONSES|
|---------|---------------|---------|
|`GET`    |data:-|Success: `200` Failure: `404`|
|`PUT`    |data:token,iets|Success: `200` Failure: `400`, `401`, `404`|
|`DELETE` |data:token,password|Success: `200` Failure: `400`, `401`, `404`|

Retrieving/creating user offers:

|METHOD   |`/user/user_id/offer`|RESPONSES|
|---------|---------------------|---------|
|`GET`    |data:-|Success: `200` Failure: `404`|
|`POST`   |data:token,iets|Success: `201` Failure: `400`, `401`|

Retrieving list of reviews of user:

|METHOD   |`/user/user_id/review`|RESPONSES|
|---------|----------------------|---------|
|`GET`    |data:-|Success: `200` Failure: `404`|

Retrieving/creating/updating/removing user reviews:

|METHOD   |`/review/offer_id`|RESPONSES|
|---------|------------------|---------|
|`GET`    |data:-|Success: `200` Failure: `404`|
|`POST`   |data:token,reviewdata|Success: `201` Failure: `400`, `401`|
|`PUT`    |data:token,reviewdata|Success: `200` Failure: `400`, `401`, `404`|
|`DELETE` |data:token|Success: `200` Failure: `401`, `404`|

Retrieving offers:

|METHOD   |`/offer?loc=X&range=X&subject_id=X&level=X&p=&sortby=X`|RESPONSES|
|---------|-------------------------------------------------------|---------|
|`GET`    |loc:, range:, subject_id:, level:, sortby:|Success: `200` Failure: `204`, `400`|

Example:
```
asd
```
