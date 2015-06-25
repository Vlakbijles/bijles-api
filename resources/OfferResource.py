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
from common.helper import postal_code_to_id
from models import User, UserMeta, Offer, PostalCode, Review, Subject, Level

from sqlalchemy import between
from sqlalchemy import and_
from sqlalchemy import case

offer_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'user.meta.name': fields.String,
    'user.meta.surname': fields.String,
    'user.meta.photo_id': fields.String,
    'level.name': fields.String,
    'subject.name': fields.String,
    'distance': fields.Integer,
    'user.meta.no_reviews': fields.Integer,
}

offersearch_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'surname': fields.String,
    'photo_id': fields.String,
    'city': fields.String,
    'level': fields.String,
    'subject': fields.String,
    'distance': fields.Float,
    'no_endorsed': fields.Integer,
    'no_reviews': fields.Integer,
}

offersearch = {
    'total_offers': fields.Integer,
    'offers': fields.Nested(offersearch_fields),
}

offer_created_fields = {
    'id': fields.Integer,
    'level_id': fields.Integer,
    'subject_id': fields.Integer,
    'level.name': fields.String,
    'subject.name': fields.String,
}


class OfferByUserIdResource(Resource):
    """
    Class for handling the GET and PUT requests for "/user/<int:id>/offer",
    which acts on offer based on their corresponding User id

    GET is used for receiving all offers linked to the User model given the User id
    POST is used for creating a new offer linked to the User model given the User id

    """

    # TODO add param to url for all or only active reviews

    @api_validation
    @marshal_with(offer_fields)
    def get(self, id):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            abort(400, message="User with id={} doesn't exist".format(id))
        offers = session.query(Offer).filter(Offer.user_id == id, Offer.active).all()

        if not offers:
            return [], 204

        return offers, 200


class OfferResource(Resource):
    """
    Class for handling the GET requests for "/offer?query"

    GET is used for receiving all offers given a searching specification,
        the search specification are:
            - postal code
            - Range around postal code, allowed distance to postal code in meters
            - Subject id
            - Level id
            - Sorting by, specifies the criteria to sort on

    """

    @api_validation
    @marshal_with(offersearch)
    def get(self):
        offer_args = offersearch_parser.parse_args()

        if not session.query(Subject).filter(Subject.id == offer_args['subject_id']).first():
            abort(400, message="Subject with id={} doesn't exist".format(offer_args['subject_id']))

        if (offer_args['level_id'] != '%') and (not session.query(Level).filter(Level.id == offer_args['level_id']).first()):
            abort(400, message="Level with id={} doesn't exist".format(offer_args['level_id']))

        # Check if given postal code is valid
        postal_code = session.query(PostalCode).\
            filter(PostalCode.postal_code_id == postal_code_to_id(offer_args['postal_code'])).first()
        if not postal_code:
            abort(400, message="Postal code ({}) not found".format(offer_args['postal_code']))

        # Cast to float for further use
        postal_code.lat = float(postal_code.lat)
        postal_code.lon = float(postal_code.lon)

        # Filter offers on subject, level and active status
        offers = session.query((Offer.id).label("id"),
                               (Subject.name).label("subject"),
                               (Level.name).label("level"), UserMeta).\
            join(Offer.user).join(User.meta).join(Offer.level).join(Offer.subject).\
            filter(Offer.active, Offer.level_id.like(offer_args['level_id']),
                   Offer.subject_id == offer_args['subject_id']).subquery()

        # Calculate distance for each offer from given postal code, and filter on given range
        offers = session.query(offers, func.round((111.045 * func.degrees(func.acos(func.cos(func.radians(postal_code.lat)) *
                           func.cos(func.radians(offers.c.latitude)) *  # NOQA
                           func.cos(func.radians(postal_code.lon - offers.c.longitude)) +
                           func.sin(func.radians(postal_code.lat)) *
                           func.sin(func.radians(offers.c.latitude))))), 2).label("distance")).\
            filter(and_(between(offers.c.latitude,
                                postal_code.lat - (200 / 111.045),
                                postal_code.lat + (200 / 111.045)),
                        between(offers.c.longitude,
                                postal_code.lon - (200 /
                                                     (111.045 * func.cos(func.radians(postal_code.lat)))),
                                postal_code.lat + (200 /
                                                     (111.045 * func.cos(func.radians(postal_code.lat))))))).subquery()

        # Calculate number of (endorsed) reviews for each user corresponding with a result offers
        offers = session.query(offers, func.count(case([(Review.desc != "", 1)])).label("no_reviews"),
                               func.count(case([(Review.endorsed, 1)])).label("no_endorsed")).\
            join(Offer, Offer.user_id == offers.c.user_id).\
            outerjoin(Review, Review.offer_id == Offer.id).\
            filter(offers.c.distance < offer_args['range']).\
            group_by(offers.c.user_id).subquery()

        total_offers = session.query(func.count(offers.c.id)).scalar()

        # Order result offers based on given argument, and add paging (8 results per page)
        if (offer_args['order_by'] == ORDER_BY_DISTANCE):
            offers = session.query(offers).order_by(offers.c.distance).\
                limit(OFFER_PAGE_SIZE).offset(8*(offer_args['page']-1)).all()
        elif (offer_args['order_by'] == ORDER_BY_NO_ENDORSED):
            offers = session.query(offers).order_by(offers.c.no_endorsed.desc()).\
                limit(OFFER_PAGE_SIZE).offset(8*(offer_args['page']-1)).all()
        elif (offer_args['order_by'] == ORDER_BY_NO_REVIEWS):
            offers = session.query(offers).order_by(offers.c.no_reviews.desc()).\
                limit(OFFER_PAGE_SIZE).offset(8*(offer_args['page']-1)).all()
        # If not specified or specified invalid, order by distance
        else:
            offers = session.query(offers).order_by(offers.c.distance).\
                limit(OFFER_PAGE_SIZE).offset(OFFER_PAGE_SIZE*(offer_args['page']-1)).all()

        result = {'total_offers': total_offers,
                  'offers': [offer._asdict() for offer in offers]}

        if not offers:
            return result, 204

        return result, 200

    @api_validation
    @authentication(None)
    @marshal_with(offer_created_fields)
    def post(self):
        offer_args = offer_parser.parse_args(data_parser("offer"))
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))

        user = session.query(User).filter(User.id == loggedin_data['user_id']).first()
        if not user:
            abort(400, message="User with id={} doesn't exist".format(id))

        subject = session.query(Subject).filter(Subject.id == offer_args['subject_id']).first()
        if not subject:
            abort(400, message="Subject with id={} doesn't exist".format(offer_args['subject_id']))

        level = session.query(Level).filter(Level.id == offer_args['level_id']).first()
        if not level:
            abort(400, message="Level with id={} doesn't exist".format(offer_args['level_id']))

        # Check if user already has this offer
        offer = session.query(Offer).filter(Offer.user_id == loggedin_data['user_id'],
                                            Offer.subject_id == offer_args['subject_id'],
                                            Offer.level_id == offer_args['level_id']).first()
        if offer:
            # If inactive, reactivate it
            if not offer.active:
                session.query(Offer).filter(Offer.id == offer.id).update({"active": True})
                return offer, 201
            else:
                return [], 200

        # Create offer when it doesn't already exist
        offer = Offer(user_id=loggedin_data['user_id'],
                      level_id=offer_args['level_id'],
                      subject_id=offer_args['subject_id'])
        session.add(offer)
        session.flush()

        return offer, 201


class OfferByIdResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/offer/<int:id>",
    acts on offers based on the Offer id

    DELETE is used for deleting an offer given the offer id. Verification is used
           to permit only deleting offers when they are yours

    """

    @api_validation
    @authentication(None)
    def delete(self, id):
        loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))

        offer = session.query(Offer).filter(Offer.id == id).first()
        if not offer:
            abort(400, message="Offer with id={} doesn't exist".format(id))

        if (offer.user.id != loggedin_data['user_id']):
            abort(401, message="Not authorized to delete offer with id={}".format(id))

        # Never actually delete offer just set active to False
        session.query(Offer).filter(Offer.id == id).update({"active": False})

        return {}, 200
