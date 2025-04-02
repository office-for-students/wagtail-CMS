import requests

from django.conf import settings


def load_course_data(institution_id, course_id, mode):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }
    base_url = "%s/institutions/%s/courses/%s/modes/%s"

    response = requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode), headers=headers)
    return response