import json, os
from django.conf import settings

from core.request_handler import get_json_file


def load_institution_json():
    response = get_json_file("institutions.json")

    if response.ok:
        response_body = response.json()
    else:
        reponse_body = {}
        
    return response_body
