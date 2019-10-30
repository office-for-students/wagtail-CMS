import json, os
from django.conf import settings


def load_institution_json():
    with open(os.path.join(settings.BASE_DIR, 'CMS/static/jsonfiles/institutions.json')) as json_file:
        data = json.load(json_file)
    return data.get('institutions')
