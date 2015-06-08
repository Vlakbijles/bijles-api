from models import User, Offer
from db import session

from flask.ext.restful import reqparse
from flask.ext.restful import request
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with


# User Resource, for actions on the User model (table)
user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String,
    'verified': fields.Boolean,
    'join_date': fields.DateTime(),
    'last_login': fields.DateTime(dt_format='iso8601'),
}

user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help="Email\
                         required")
user_parser.add_argument('password', type=str, required=True, help="Password\
                         required")


class UserResource(Resource):
    @marshal_with(user_fields)
    # delete is used for giving info about a user model
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        print user.offers[0].subject.name

        return user, 201

    # delete is used for deleting a user model
    def delete(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        session.delete(user)
        session.commit()
        return {}, 204

    # post is used for creating a user model
    @marshal_with(user_fields)
    def post(self, id):
        args = user_parser.parse_args()
        user = User(email=args['email'], password=args['password'])
        session.add(user)
        session.commit()
        return user, 201

    # put is used for updating a user model
    @marshal_with(user_fields)
    def put(self, id):
        args = user_parser.parse_args()
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        # if user exists, see which data is sent and change user accordingly
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.password = args['password']
        session.add(user)
        session.commit()
        return user, 201


class UserOfferResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        todos = session.query(User).all()
        return todos

    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        todo = User(task=args['task'])
        session.add(todo)
        session.commit()
        return todo, 201
