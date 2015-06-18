#!/usr/bin/env python
"""
OfferResource.py, for actions on the Offer model which is related to the User model.
this file is a module and has no use as stand-alone file

Offer Resouces contains the following classes:
- OfferByUserIdResource, acts on Offers based on the User id
- OfferResource, acts on all Offers (e.g. searching)
- OfferByIdResource, acts on a Offer based on the Offer id

"""


from resources import *  # NOQA
from common.helper import latlon_distance, zipcode_to_id
from models import User, Offer, Zipcode, Review, Subject, Level


offer_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'user.meta.name': fields.String,
    'user.meta.surname': fields.String,
    'level.name': fields.String,
    'subject.name': fields.String,
    'distance': fields.Integer,
    'user.meta.rating': fields.Float,
    'user.meta.no_reviews': fields.Integer,
}


class OfferByUserIdResource(Resource):
    """
    Class for handling the GET and PUT requests for "/user/<int:id>/offer",
    which acts on offer based on their corresponding User id

    GET is used for receiving all offers linked to the User model given the User id
    POST is used for creating a new offer linked to the User model given the User id

    """

    def __init__(self):
        # Parse all class-wide used data
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @marshal_with(offer_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(401, message="User with id={} doesn't exist".format(id))
        offers = session.query(Offer).filter(Offer.user_id == id, Offer.active).all()
        if not offers:
            return [], 204

        return offers, 200


class OfferResource(Resource):
    """
    Class for handling the GET requests for "/offer?query"

    GET is used for receiving all offers given a searching specification,
        the search specification are:
            - Location's latitude and longitude given in degrees
            - Range around location, allowed distance to location in meters
            - Subject, id of the subject
            - Level, id of the level
            - Sorting by, specifies the criteria to sort on

    """

    def __init__(self):
        # Parse all class-wide used data
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @marshal_with(offer_fields)
    def get(self):
        offer_query = offersearch_parser.parse_args()
        offers = session.query(Offer).filter(Offer.subject_id == offer_query['subject'],
                                             Offer.level_id == offer_query['level']).all()

        subject = session.query(Subject).filter(Subject.id == (offer_query['subject'])).first()
        if not subject:
            abort(400, message="Subject with id {} not found".format(offer_query['subject']))

        zipcode = session.query(Zipcode).filter(Zipcode.zipcode_id == zipcode_to_id(offer_query['loc'])).first()
        if not zipcode:
            abort(400, message="Zipcode ({}) not found".format(offer_query['loc']))
        loc_lat = float(zipcode.lat)
        loc_lon = float(zipcode.lon)

        result_offers = []

        # Check which offers are within given range and calculate their average rating
        for offer in offers:
            offer_lat = float(offer.user.meta.latitude)
            offer_lon = float(offer.user.meta.longitude)
            if latlon_distance(loc_lat, loc_lon, offer_lat, offer_lon) < offer_query['range']:
                offer.distance = latlon_distance(loc_lat, loc_lon, offer_lat, offer_lon)
                offer.user.meta.rating = session.query(func.avg(Review.rating).label('rating_avg')).join(Review.offer).filter(Offer.user_id == offer.user.id).first()[0]
                offer.user.meta.no_reviews = session.query(func.count(Review.rating).label('rating_avg')).join(Review.offer).filter(Offer.user_id == offer.user.id).first()[0]
                result_offers.append(offer)

        if not result_offers:
            abort(404, message="No offers found")

        return result_offers, 200

    @api_validation
    @authentication(None)
    def post(self):
        offer_args = offer_parser.parse_args(data_parser("offer", self.args))
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin", self.args))

        user = session.query(User).filter(User.id == loggedin_data['user_id']).first()
        if not user:
            abort(404, message="User with id={} doesn't exist".format(id))

        subject = session.query(Subject).filter(Subject.id == offer_args['subject_id']).first()
        if not subject:
            abort(404, message="Subject with id={} doesn't exist".format(offer_args['subject_id']))

        level = session.query(Level).filter(Level.id == offer_args['level_id']).first()
        if not level:
            abort(404, message="Level with id={} doesn't exist".format(offer_args['level_id']))

        offer = get_or_create(session, Offer, user_id=loggedin_data['user_id'],
                              level_id=offer_args['level_id'],
                              subject_id=offer_args['subject_id'],
                              active=True)

        session.add(offer)
        session.commit()
        return {}, 201


class OfferByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/offer/<int:id>",
    acts on offers based on the Offer id

    DELETE is used for deleting a offer given the offer id. Verification is used
           to permit only deleting offers when they are yours

    """

    def __init__(self):
        # Parse all class-wide used data
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @authentication(None)
    def delete(self, id):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin", self.args))

        offer = session.query(Offer).filter(Offer.id == id).first()
        if not offer:
            abort(404, message="Offer with id={} doesn't exist".format(id))

        if (offer.user.id != loggedin_data['user_id']):
            abort(401, message="Not authorized to delete offer with id={}".format(id))

        # Only delete offers with no reviews linked to them, otherwise deactivate
        review = session.query(Review).filter(Review.offer_id == id).first()
        if not review:
            session.delete(offer)
            session.commit()
        else:
            session.query(Offer).filter(Offer.id == id).update({"active": False})
            session.commit()

        return {}, 200
