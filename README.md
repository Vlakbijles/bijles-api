# Suftware - Bijles Platform
Dit is een markplaats voor bijles. Je kunt hier zowel bijles aanbieden als
aanvragen.

# Chat
[Chat](https://vlakbijles.slack.com)

# Authentication

### Client
Every API client has a unique alphanumerical username and a private 128-bit
key. To set up a privileged API request first set up the following JSON object:

```
{
    "api_user": username,
    "data": {
                ...
            }
    "timestamp": utc_timestamp,
}
```

Now flatten the JSON object above to a string `data_json` and make sure the
keys are sorted alphabetically (in python this can be done by calling
`json.dumps(data_dict, sort_keys=True)`). The next step generates a SHA256 HMAC
hash for the current API request using `data_json`, the HTTP URI (string of
requested path, including leading `/`) and the HTTP method in the following
order (Python example):

```
import hmac
from hashlib import sha256
hash = hmac.new(private_key, data_json, sha256)
hash.update(http_uri)
hash.update(http_method)
```

Now add the generated hash to the original JSON object, flatten, alphabetically
sort by key and set up the resulting HTTP request:

```
METHOD URI HTTP/1.1
Content-Type: application/json

{"api_user": username, "data": { ... }, "hash": hash, "timestamp": utc_timestamp,}
```

### Server
Has access to the list of API clients and their keys, roughly reverses the
process described above to verify the request. The addition of a timestamp in
the request data provides the server with a means of preventing _replay
attacks_ since the hash calculation includes the timestamp.
