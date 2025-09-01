import requests

from CMS.test.mocks.institution_mocks import InstitutionMocks
from core.mongo import Mongo
from django.conf import settings


def load_institution_data(institution_id):

    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }
    base_url = "%s/institutions/%s"

    return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id), headers=headers)