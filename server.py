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

from hashlib import sha256

from os import urandom

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

db_con = None           # MySQLdb connection
db_cur = None           # MySQLdb cursor
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
        if utc_now - timestamp < 10:

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



def create_token(user_id):
    """
    Generate new token, add to db

    """
    utc_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    expiration_date = utc_now + 604800 # 7 days

    print user_id
    print expiration_date

    token_hash = hmac.new(str(user_id), str(expiration_date), sha256)
    token_hash.update(urandom(64))
    token_digest = token_hash.hexdigest()

    db_cur.execute("INSERT INTO token (user_id, hash, expiration_date) \
                    VALUES ({}, '{}', {})".format(user_id, token_digest,
                                                  expiration_date))
    db_con.commit()

    return token_digest


def login(email, password):

    db_cur.execute("SELECT id, password FROM user WHERE email = '{}'".format(email))
    data = db_cur.fetchone()

    if data:
        if data[1] == password:
            return True, create_token(data[0])

    return False, None


def login_check(user_id, token):
    """
    Returns boolean accompanied by old/renewed token/None object
    """

    db_cur.execute("SELECT hash, expiration_date FROM token \
                    WHERE user_id = {}".format(user_id))
    data = db_cur.fetchall()

    if data:
        for row in data:

            token_db = row[0]

            if token_db == token:

                expiration_date = row[1]
                utc_now = int(time.mktime(datetime.datetime.utcnow().timetuple()))

                # If token is expired, create a new one, remove old one
                if utc_now - expiration_date > 0:
                    db_cur.execute("DELETE FROM token WHERE hash = {}".format(token))
                    db_con.commit()
                    token = create_token(user_id)

                return True, token

    return False, None



class UserCreator(Resource):

    def post(self):
        if verify_request(request.path, request.method, request.data):
            return {"message":"New user succesfully created", "status":"201"}, 201
            return {"message":"Something went wrong", "status":"409"}, 409
        else:
            return {"message":"Unauthorized request", "status":"401"}, 401


class User(Resource):

    def get(self, user_id):
        if verify_request(request.path, request.method, request.data):
            db_cur.execute("SELECT * FROM user WHERE id = {}".format(user_id))
            data = db_cur.fetchone()
            if data:
                data = [str(e) for e in list(data)]
            if data:
                column_names = [d[0] for d in db_cur.description]
                return dict(zip(column_names, data)), 200
            else:
                return {"message":"User not found", "status":"404"}, 404
        else:
            return {"message":"Unauthorized request", "status":"401"}, 401

    def delete(self, user_id):
        if verify_request(request.path, request.method, request.data):
            return {"200": "User succesfully deleted"}, 200
        else:
            return {"message":"Unauthorized request", "status":"401"}, 401

    def put(self, user_id):
        if verify_request(request.path, request.method, request.data):
            return {"200": "User succesfully updated"}, 200
        else:
            return {"message":"Unauthorized request", "status":"401"}, 401


if __name__ == '__main__':
    if load_config("config/config.cfg") and load_keys("config/api_users.cfg"):

        try:
            db_con = MySQLdb.connect(host=config["db_host"],
                                   port=config["db_port"],
                                   user=config["db_user"],
                                   passwd=config["db_passwd"],
                                   db=config["db_name"])
            db_cur = db_con.cursor()
        except:
            print("Unable to connect to mysql server")
        else:

            # Start API server over https
            # context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            # context.load_cert_chain('ssl.cert', 'ssl.key')
            # app.run(host=host, port=port, debug=False, ssl_context=context,
            #         use_reloader=False)

            api.add_resource(UserCreator, "/user")
            api.add_resource(User, "/user/<int:user_id>")
            app.run(host=config["host"], port=config["port"], debug=True,
                    use_reloader=False)
