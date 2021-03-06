"""
    LevelResource.py

    LevelResource contains the following classes:
        -LevelResource, used for returning list of levels, requires no API authorization

"""


from resources import *  # NOQA
from models import Level


level_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


class LevelResource(Resource):
    """
    Class for handling the GET requests to "/level/all"

    GET is used to get all levels

    """

    @api_validation
    @marshal_with(level_fields)
    def get(self):
        levels = session.query(Level).all()

        if not levels:
            abort(204, message="No levels found")

        # TODO remove extra header in final, temporarily allows cross-site ajax
        return levels, 200, {"Access-Control-Allow-Origin": "*"}
