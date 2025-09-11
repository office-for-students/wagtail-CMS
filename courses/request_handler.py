import requests

from CMS.test.mocks.course_format_mocks import CourseFormatMocks
from CMS.test.mocks.course_mocks import CourseMocks
from CMS.test.mocks.joint_course_format_mocks import JointCourseFormatMocks

from core.mongo import Mongo
from django.conf import settings


def load_course_data(institution_id, course_id, mode):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }
    base_url = "%s/institutions/%s/courses/%s/modes/%s"

    response = requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
    return response