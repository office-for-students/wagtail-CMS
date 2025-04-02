import requests

from django.conf import settings


def load_institution_data(institution_id):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }
    base_url = "%s/institutions/%s"

    return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id), headers=headers)