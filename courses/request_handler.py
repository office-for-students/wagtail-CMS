import requests

from django.conf import settings

from CMS.test.mocks import NewCourseFormatMocks, CourseMocks
from CMS.test.joint_course_mocks import NewJointCourseFormatMocks


def load_course_data(institution_id, course_id, mode):
    # if True or settings.LOCAL:
    if settings.LOCAL:
        if course_id == "GN12":
            return NewJointCourseFormatMocks.get_successful_course_load_response()
        return NewCourseFormatMocks.get_successful_course_load_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s/courses/%s/modes/%s"

        # TODO Print statement added for debugging purposes. Delete before deploying to PROD
        # print(requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers).content.decode("utf8"))

        return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
