#!/usr/bin/env python2

# Possible features:
# - cache requests

import ssl
import ConfigParser
import MySQLdb
import hmac
import time
import datetime
import json

from flask import Flask, request, jsonify
from flask.views import MethodView
from hashlib import sha256


app = Flask(__name__)
db = None               # MySQLdb database cursor
api_users = None        # API username/key dict
config = {}             # Settings dict


def load_config(filename):
    global config
    try:
        config_file = ConfigParser.SafeConfigParser()
        config_file.read(filename)
        config["host"] = config_file.get("server", "host")
        config["port"] = int(config_file.get("server", "port"))
        config["ssl_cert"] = config_file.get("server", "ssl_cert")
        config["ssl_key"] = config_file.get("server", "ssl_key")
        config["db_host"] = config_file.get("mysql", "host")
        config["db_port"] = int(config_file.get("mysql", "port"))
        config["db_user"] = config_file.get("mysql", "user")
        config["db_passwd"] = config_file.get("mysql", "passwd")
        config["db_name"] = config_file.get("mysql", "db")
    except:
        print("Error parsing config file")
        return False
    return True


def load_keys(filename):
    global api_users
    try:
        with open(filename) as file:
            api_users = json.load(file)
    except:
        print("Error parsing keys file")
        return False
    return True


def verify_request(uri, method, data):
    """
    Verify request using HMAC by reconstructing the hash with the provided
    data and comparing it to the provided hash

    """

    try:
        data_dict = json.loads(data)
        api_user = data_dict["api_user"]
        timestamp = int(data_dict["timestamp"])
        provided_hash = data_dict["hash"]
    except:
        return False
    else:

        # Ignore 'old' requests
        utc_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if utc_now - timestamp < 60:

            if api_user in api_users:
                key = api_users[api_user]

                # Remove hash field from json data in order to regenerate
                # original hash
                del data_dict["hash"]
                data_json = json.dumps(data_dict, sort_keys=True)

                reconstructed_hash = hmac.new(str(key), data_json, sha256)
                reconstructed_hash.update(uri)
                reconstructed_hash.update(method)
                return reconstructed_hash.hexdigest() == provided_hash

    return False


@app.errorhandler(404)
def not_implemented(error=None):
    return respond({"501": "Unable to fulfill request"}, 501)


def respond(data, status_code):
    response = jsonify(data)
    response.status_code = status_code
    return response


class UserAPI(MethodView):

    def get(self, user_id):
        """ Return user information """
        db.execute("SELECT * FROM user WHERE id = {}".format(user_id))
        data = db.fetchone()
        if data:
            column_names = [d[0] for d in db.description]
            return respond(dict(zip(column_names, data)), 200)
        else:
            return respond({"404": "User not found"}, 404)

    def post(self):
        """ Create new user """
        if verify_request(request.path, request.method, request.data):
            return respond({"201": "New user succesfully created"}, 201)
            return respond({"409": "Something went wrong, please check data"},
                           409)
        else:
            return respond({"401": "Unauthorized request"}, 401)

    def delete(self, user_id):
        """ Delete existing user """
        if verify_request(request.path, request.method, request.data):
            return respond({"200": "User succesfully deleted"}, 200)
        else:
            return respond({"401": "Unauthorized request"}, 401)

    def put(self, user_id):
        """ Update user fields """
        if verify_request(request.path, request.method, request.data):
            return respond({"200": "User succesfully updated"}, 200)
        else:
            return respond({"401": "Unauthorized request"}, 401)


if __name__ == '__main__':
    if load_config("config/config.cfg") and load_keys("config/api_users.cfg"):

        try:
            conn = MySQLdb.connect(host=config["db_host"],
                                   port=config["db_port"],
                                   user=config["db_user"],
                                   passwd=config["db_passwd"],
                                   db=config["db_name"])
            db = conn.cursor()
        except:
            print("Unable to connect to mysql server")
        else:

            # Start API server over https
            # context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            # context.load_cert_chain('ssl.cert', 'ssl.key')
            # app.run(host=host, port=port, debug=False, ssl_context=context,
            #         use_reloader=False)

            user_view = UserAPI.as_view("user_api")
            app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
            app.add_url_rule("/user/<int:user_id>", view_func=user_view,
                             methods=["DELETE", "PUT", "GET"])

            app.run(host=config["host"], port=config["port"], debug=True,
                    use_reloader=False)
