"""
TODO

"""


from resources import *  # NOQA
from models import Subject


subject_fields = {
    'id': fields.Integer,
    'name': fields.String(),
}


class SubjectResource(Resource):
    """
    Class for handling the GET requests for "/subject/all"

    GET is used for retrieving all subjects

    """

    def __init__(self):
        pass

    # @api_validation
    @marshal_with(subject_fields)
    def get(self):
        subjects = session.query(Subject).all()

        if not subjects:
            abort(404, message="No subjects found")

        return subjects, 200
