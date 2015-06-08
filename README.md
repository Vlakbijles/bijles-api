Vlakbijles API
===================

Requirements:
    - flask
    - flask-restful
    - sqlalchemy

# API Protocol
The following requests require content type json, following format, data only on post/put/delete

```
{
    "api_user": api_user,
    "data" = {
               ..
             },
    "hash": hash,
    "timestamp": timestamp
}
```

|METHOD   |`/user`|RESPONSES|
|---------|-------|---------|
|`GET`    |-|-|
|`POST`   |data:iets|Success: `201` Failure: `400`|
|`PUT`    |-|-|
|`DELETE` |-|-|

|METHOD   |`/user/user_id`|RESPONSES|
|---------|---------------|---------|
|`GET`    |empty data field|Success: `200` Failure: `404`|
|`POST`   |-|-|
|`PUT`*   |data:token,iets|Success: `200` Failure: `400, 404`|
|`DELETE`*|data:token,password|Success: `200` Failure: `400, 404`|

|METHOD   |`/user/user_id/offer`|RESPONSES|
|---------|---------------------|---------|
|`GET`*   |data:token|Success: `` Failure: ``|
|`POST`*  |data:token,iets|Success: `` Failure: ``|
|`PUT`    |-|-|
|`DELETE`*|data:token,password|Success: `` Failure: ``|

|METHOD   |`/user/user_id/review`|RESPONSES|
|---------|----------------------|---------|
|`GET`*   |data:token|Success: `` Failure: ``|
|`POST`   |-|-|
|`PUT`    |-|-|
|`DELETE` |-|-|

|METHOD   |`/review/offer_id`|RESPONSES|
|---------|------------------|---------|
|`GET`    |data:token|Success: `` Failure: ``|
|`POST`   |data:token,reviewdata|Success: `` Failure: ``|
|`PUT`    |data:token,reviewdata|Success: `` Failure: ``|
|`DELETE` |data:token|Success: `` Failure: ``|

Example:
```asdd```

The following request does not use the http data field:
|METHOD   |`/offer?loc=X&range=X&subject_id=X&level=X&p=&sortby=X`|RESPONSES|
|---------|-------------------------------------------------------|---------|
|`GET`    |loc:, range:, subject_id:, level:, sortby:|Success: `200` Failure: `404`|
|`POST`   |-|-|
|`PUT`    |-|-|
|`DELETE` |-|-|
