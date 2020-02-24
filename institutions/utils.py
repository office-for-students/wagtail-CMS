import json, os
from django.conf import settings
from CMS.enums import enums

from core.request_handler import get_json_file


def load_institution_json():
    institution_json = {}

    for language, language_full in enums.languages_map.items():
        response = get_json_file("institutions_" + language + ".json")

        if response.ok:
            response_body = response.json()
        else:
            response_body = {}

        institution_json[language] = response_body
        
    return institution_json
  