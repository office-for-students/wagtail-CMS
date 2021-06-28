import json
from requests.models import Response
from http import HTTPStatus

from CMS.test.mocks.joint_course_format_mocks_content import content

class JointCourseFormatMocks:

    @classmethod
    def get_successful_course_load_content(cls):
        return content

    @classmethod
    def get_successful_course_load_response(cls):
        response = Response()
        response.status_code = HTTPStatus.OK
        response._content = json.dumps(cls.get_successful_course_load_content()).encode('utf-8')
        return response
