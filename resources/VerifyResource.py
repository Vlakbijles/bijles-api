#!/usr/bin/env python
"""
    VerifyResource.py, for checking valid form input
    this file is a module and has no use as stand-alone file

    VerifyResource contains the following classes:
    - Verify

"""


from resources import *  # NOQA
from models import User


class VerifyResource(Resource):
    """
    Class for handling the GET, PUT and DELETE requests for "/verify?"

    GET is used for checking whether the input is valid

    """

    @api_validation
    def get(self):
        args = verify_parser.parse_args()

        if (args['verify_type'] == "email"):
            if (self.data['data'] and ("loggedin" in self.data['data'])):
                loggedin_data = loggedin_parser.parse_args(data_parser("loggedin"))
                user = session.query(User).filter(User.id != loggedin_data['user_id'],
                                                  User.email == args['verify_data']).first()
            else:
                user = session.query(User).filter(User.email == args['verify_data']).first()

            if user:
                abort(400, message="Email ({}) is already in use".format(args['verify_data']))
            return {}, 200
        elif (args['verify_type'] == "postal_code"):
            postal_code = session.query(PostalCode).filter(PostalCode.postal_code == args['verify_data']).first()
            if not postal_code:
                abort(400, message="Postal code ({}) not found".format(postal_code.postal_code))
            return {}, 200
