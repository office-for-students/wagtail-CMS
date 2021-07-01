import requests

from CMS.test.mocks.course_format_mocks import CourseFormatMocks
from CMS.test.mocks.course_mocks import CourseMocks
from CMS.test.mocks.joint_course_format_mocks import JointCourseFormatMocks

from core.mongo import Mongo
from django.conf import settings


def load_course_data(institution_id, course_id, mode):
    if settings.LOCAL:
        if course_id == "GN12":
            return JointCourseFormatMocks.get_successful_course_load_response()
        return CourseFormatMocks.get_successful_course_load_response()
    if settings.MONGODB_HOST:
        print("mongo")
        mongo = Mongo('courses')
        return mongo.get_one(
            {
                'institution_id': str(institution_id),
                'course_id': str(course_id),
            }
        )
    else:
        print("application")
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s/courses/%s/modes/%s"

        response = requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
        return response
