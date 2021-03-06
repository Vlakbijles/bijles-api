"""
    SubjectResource.py

    SubjectResource contains the following classes:
        -SubjectResource, used for returning list of subjects, requires no API authorization

"""


from resources import *  # NOQA
from models import Subject


subject_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


class SubjectResource(Resource):
    """
    Class for handling the GET requests to "/subject/all"

    GET is used to get all subjects
    """

    @api_validation
    @marshal_with(subject_fields)
    def get(self):
        subjects = session.query(Subject).all()

        if not subjects:
            abort(204, message="No subjects found")

        # TODO remove extra header in final, temporarily allows cross-site ajax
        return subjects, 200, {"Access-Control-Allow-Origin": "*"}
