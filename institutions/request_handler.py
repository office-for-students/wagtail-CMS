import requests

from django.conf import settings

from CMS.test.mocks import InstitutionMocks


def load_institution_data(institution_id):
    if settings.LOCAL:
        return InstitutionMocks.get_successful_institution_load_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s"

        return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id), headers=headers)
