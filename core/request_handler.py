import requests

from django.conf import settings


def send_feedback(feedback_data):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.post(url=settings.FEEDBACK_API_HOST, headers=headers, data=feedback_data)


def get_json_file(json_file):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.get(url=settings.JSONFILES_STORAGE_CONTAINER + "/" + json_file, headers=headers)