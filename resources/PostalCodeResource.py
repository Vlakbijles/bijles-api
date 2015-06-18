"""
    LevelResource.py

    LevelResource contains the following classes:
        -LevelResource, used for returning list of levels, requires no API authorization

"""


from resources import *  # NOQA
from models import Zipcode


postal_code_fields = {
    'zipcode': fields.String,
}


class PostalCodeResource(Resource):
    """
    Class for handling the GET requests to "/postal_code/all"

    GET is used to get all levels

    """

    def __init__(self):
        self.method = request.method
        self.full_path = request.full_path
        self.args = main_parser.parse_args()

    @api_validation
    @marshal_with(postal_code_fields)
    def get(self):
        postal_codes = session.query(Zipcode).all()

        if not postal_codes:
            abort(404, message="No postal codes found")

        # TODO remove extra header in final, temporarily allows cross-site ajax
        return postal_codes, 200, {"Access-Control-Allow-Origin": "*"}

