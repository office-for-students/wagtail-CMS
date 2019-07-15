import json
from requests.models import Response
from http import HTTPStatus


class SearchMocks:

    @classmethod
    def get_search_response_content(cls):
        return {
            "total_number_of_courses": 10,
            "total_results": 5,
            "items": [
                {
                    'id': 1,
                    'institution': 'Oxford',
                    'course_name': 'Farming'
                }
            ]
        }

    @classmethod
    def get_successful_search_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_search_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_search_response(cls):
        response = Response()
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
        return response
