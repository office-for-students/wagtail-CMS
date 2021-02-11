import requests

from CMS.test.mocks import InstitutionMocks
from core.mongo import Mongo
from django.conf import settings


def load_institution_data(institution_id):

    if settings.LOCAL:
        return InstitutionMocks.get_successful_institution_load_response()
    if settings.MONGODB_HOST:
        mongo = Mongo('institutions')
        return mongo.get_one({'institution_id': str(institution_id)})
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s/institutions/%s"

        return requests.get(url=base_url % (settings.DATASETAPIHOST, institution_id), headers=headers)
