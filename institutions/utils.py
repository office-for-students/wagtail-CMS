import json, os
from django.conf import settings

from core.request_handler import get_json_file


def load_institution_json():
    institutions = {}
        
    response = get_json_file("institutions_en.json")

    if response.ok:
        response_body = response.json()
    else:
        reponse_body = {}

    institutions["en"] = response_body

    response = get_json_file("institutions_cy.json")

    if response.ok:
        response_body = response.json()
    else:
        reponse_body = {}

    institutions["cy"] = response_body


    return institutions
