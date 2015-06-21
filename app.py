#!/usr/bin/env python2

from flask import Flask
from flask.ext.restful import Api

from common.db import session

from config import server

app = Flask(__name__)
api = Api(app)

from resources.UserResource import UserByIdResource, UserResource
from resources.OfferResource import OfferByUserIdResource, OfferResource, OfferByIdResource
from resources.FbLoginResource import FbLoginResource
from resources.ReviewResource import ReviewByUserIdResource, ReviewResource
from resources.SubjectResource import SubjectResource
from resources.LevelResource import LevelResource
from resources.TestResource import TestResource

# Routes
# User
api.add_resource(UserByIdResource, '/user/<int:id>')
api.add_resource(UserResource, '/user')

# Login
api.add_resource(FbLoginResource, '/fblogin')

# Offer
api.add_resource(OfferResource, '/offer')
api.add_resource(OfferByUserIdResource, '/user/<int:id>/offer')
api.add_resource(OfferByIdResource, '/offer/<int:id>')

# Review
api.add_resource(ReviewByUserIdResource, '/user/<int:id>/review')
api.add_resource(ReviewResource, '/review')

# Subjects
api.add_resource(SubjectResource, '/subject/all')

# Levels
api.add_resource(LevelResource, '/level/all')

# Test
api.add_resource(TestResource, '/test')


@app.teardown_request
def shutdown_session(response_or_exc):
    if response_or_exc is None:
        session.commit()
    session.remove()
    return response_or_exc

if __name__ == '__main__':
    # app.run(host=server["host"], port=server["port"])
    app.run(host=server["host"], port=server["port"], debug=True)
