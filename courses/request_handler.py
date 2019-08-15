import requests

from django.conf import settings

from CMS.test.mocks import CourseMocks


def load_course_data(institution_id, course_id, mode):
    if settings.LOCAL:
        return CourseMocks.get_successful_course_load_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s/courses/%s/modes/%s"

        return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
