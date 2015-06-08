#!/usr/bin/env python2

from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)
api = Api(app)

from resources import UserResource

api.add_resource(UserResource, '/user/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
