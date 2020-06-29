import requests

from django.conf import settings

from CMS.test.mocks import NewCourseFormatMocks, CourseMocks


def load_course_data(institution_id, course_id, mode):
    if True or settings.LOCAL:
    # if settings.LOCAL:
        return NewCourseFormatMocks.get_successful_course_load_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s/courses/%s/modes/%s"

        # print(requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers).content.decode("utf8"))

        return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
