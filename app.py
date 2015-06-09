#!/usr/bin/env python2

from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)
api = Api(app)

from resources.UserResource import UserByIdResource, UserResource
from resources.OfferResource import OfferByUserIdResource, OfferResource

# Routes
# User
api.add_resource(UserByIdResource, '/user/<int:id>')
api.add_resource(UserResource, '/user')

# Offer
api.add_resource(OfferResource, '/offer')
api.add_resource(OfferByUserIdResource, '/user/<int:id>/offer')

if __name__ == '__main__':
    app.run(debug=True)
