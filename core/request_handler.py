import requests

from django.conf import settings


def send_feedback(feedback_data):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.post(url=settings.FEEDBACK_API_HOST, headers=headers, data=feedback_data)
