import json
from requests.models import Response
from http import HTTPStatus

from CMS.test.mocks.institution_mocks_content import content

class InstitutionMocks:
    @classmethod
    def get_successful_institution_load_content(cls):
        return content

    @classmethod
    def get_successful_institution_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_institution_load_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_institution_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
        return response
