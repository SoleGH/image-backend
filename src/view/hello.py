from view.common import PathViewV1
from flask_restful import reqparse


class Hello(PathViewV1):
    _path = "/api/v1/hello"

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('param', type=str, required=False, location='args')
        data = parser.parse_args()
        return self.response_success_dict(**data)


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('post_p', type=str, required=True, location='json')
        data = parser.parse_args()

        return self.response_success_dict(**data)