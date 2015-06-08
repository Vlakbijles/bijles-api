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
|`GET`    |loc:, range:, subject_id:, level:, sortby:|Success: `200` Failure: `204`, `400`|

Example:
```
asd
```
