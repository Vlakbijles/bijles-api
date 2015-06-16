"""
SubjectResource.py

For returning list of subjects, requires no API authorization

"""


from resources import *  # NOQA
from models import Subject


subject_fields = {
    'id': fields.Integer,
    'name': fields.Raw, # Not fields.String, can contain crazy characters
}


class SubjectResource(Resource):
    """
    Class for handling the GET requests to "/subject/all"

    """

    def __init__(self):
        pass

    @marshal_with(subject_fields)
    def get(self):
        subjects = session.query(Subject).all()

        if not subjects:
            abort(404, message="No subjects found")

        return subjects, 200
