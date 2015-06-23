#!/usr/bin/env python
"""
    ReviewResource.py, for actions on the Review model,
    this file is a module and has no use as stand-alone file

    ReviewResource contains the following classes:
        -ReviewByUserIdResource, used for getting the review for a User
"""


from resources import *  # NOQA
from models import User, Review, Offer


review_fields = {
    'endorsed': fields.Boolean,
    'description': fields.String,
    'date': fields.DateTime,
    'author.id': fields.Integer,
    'author.meta.photo_id': fields.String,
    'author.meta.name': fields.String,
    'author.meta.surname': fields.String,
    'offer.subject.name': fields.String,
    'offer.level.name': fields.String,
}

endorsment_fields = {
    'author.id': fields.Integer,
    'author.meta.photo_id': fields.String,
    'author.meta.name': fields.String,
    'author.meta.surname': fields.String,
}


class ReviewByUserIdResource(Resource):
    """
    Class for handling the GET "/user/<int:id>/review"

    GET is used to get the reviews for a User model, given a User id

    """

    @api_validation
    @marshal_with(review_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(204, message="User with id={} doesn't exist".format(id))

        reviews = session.query(Review).join(Review.offer).\
            filter(Offer.user_id == id).order_by(Review.date).all()

        return reviews, 200


class EndorsmentByUserIdResource(Resource):
    """
    Class for handling the GET "/user/<int:id>/endorsment

    GET is used to get a list of users who endorse the provided user

    """

    @api_validation
    @marshal_with(endorsment_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(204, message="User with id={} doesn't exist".format(id))

        endorsments = session.query(Review).join(Review.offer).join(Offer.user).\
            filter(Review.endorsed, User.id == id).group_by(Review.author_id).all()

        if endorsments:
            return endorsments, 200
        else:
            return [], 204


class ReviewResource(Resource):
    """
    Class for handling POST "/review"

    POST is used to create reviews

    """

    @api_validation
    @authentication(None)
    @marshal_with(review_fields)
    def post(self):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))
        review_data = review_parser.parse_args(data_parser("review"))

        # Check if offer exists
        offer = session.query(Offer).filter(Offer.id == review_data["offer_id"]).first()
        if not offer:
            abort(400, message="Offer with id={} doesn't exist".format(review_data["offer_id"]))

        # Check if user is about to review himself
        if offer.user_id == loggedin_data["user_id"]:
            abort(400, message="Not allowed to review own offer")

        # Check if user has already reviewed this offer
        if session.query(Review).filter(Review.offer_id == offer.id,
                                        Review.author_id == loggedin_data["user_id"]).first():
            return [], 200

        # Create review
        review = Review(offer_id=offer.id,
                        author_id=loggedin_data["user_id"],
                        endorsed=review_data["endorsed"])

        if review_data["description"]:
            # Check if description exceeds max length
            if len(review_data["description"]) > 500:
                abort(400, message="Description exceeded max length of 500 chars")
            review.description = review_data["description"]

        session.add(review)
        session.flush()

        return review, 201
