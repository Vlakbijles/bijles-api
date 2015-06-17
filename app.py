#!/usr/bin/env python2

from flask import Flask
from flask.ext.restful import Api

from config import server

app = Flask(__name__)
api = Api(app)

from resources.UserResource import UserByIdResource, UserResource
from resources.OfferResource import OfferByUserIdResource, OfferResource, OfferByIdResource
from resources.LoginResource import LoginResource
from resources.FbLoginResource import FbLoginResource
from resources.ReviewResource import ReviewByUserIdResource
from resources.SubjectResource import SubjectResource

# Routes
# User
api.add_resource(UserByIdResource, '/user/<int:id>')
api.add_resource(UserResource, '/user')

# Login
api.add_resource(LoginResource, '/login')
api.add_resource(FbLoginResource, '/fblogin')

# Offer
api.add_resource(OfferResource, '/offer')
api.add_resource(OfferByUserIdResource, '/user/<int:id>/offer')
api.add_resource(OfferByIdResource, '/offer/<int:id>')

# Review
api.add_resource(ReviewByUserIdResource, '/user/<int:id>/review')

# Subject
api.add_resource(SubjectResource, '/subject/all')

if __name__ == '__main__':
    app.run(host=server["host"], port=server["port"], debug=True)
