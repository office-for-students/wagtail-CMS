import requests

from CMS.test.mocks import NewCourseFormatMocks, CourseMocks
from CMS.test.joint_course_mocks import NewJointCourseFormatMocks

from core.mongo import Mongo
from django.conf import settings


def load_course_data(institution_id, course_id, mode):
    if settings.LOCAL:
        if course_id == "GN12":
            return NewJointCourseFormatMocks.get_successful_course_load_response()
        return NewCourseFormatMocks.get_successful_course_load_response()
    if settings.MONGODB_HOST:
        mongo = Mongo('courses')
        return mongo.get_one(
            {
                'institution_id': institution_id,
                'course_id': course_id,
            }
        )
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s/courses/%s/modes/%s"

        response = requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
        return response
