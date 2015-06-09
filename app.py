#!/usr/bin/env python2

from flask import Flask
from flask.ext.restful import Api

from config import config

app = Flask(__name__)
api = Api(app)

from resources.UserResource import UserByIdResource, UserResource
from resources.OfferResource import OfferByUserIdResource

# Routes
# User
api.add_resource(UserByIdResource, '/user/<int:id>')
api.add_resource(UserResource, '/user')

# Offer
api.add_resource(OfferByUserIdResource, '/user/<int:id>/offer')

if __name__ == '__main__':
    app.run(host=config["server"]["host"], port=config["server"]["port"], debug=True)
