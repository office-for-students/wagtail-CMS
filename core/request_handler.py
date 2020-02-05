import json, os
import requests

from django.conf import settings

def send_feedback(feedback_data):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.post(url=settings.FEEDBACK_API_HOST, headers=headers, data=feedback_data)


def get_json_file(json_file):

    if settings.JSONFILES_STORAGE_CONTAINER == "":
        print("Loading local jsonfile")
        with open(os.path.join(settings.BASE_DIR, 'CMS/static/jsonfiles/' + json_file)) as json_file:
            data = json_file.read()

        response = requests.Response()

        response_state = response.__getstate__()
        response_state["status_code"] = 200
        response_state["_content"] = data.encode('utf-8')
        response_state["encoding"] = 'utf-8'
        
        response.__setstate__(response_state)

        return response
        
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.get(url=settings.JSONFILES_STORAGE_CONTAINER + "/" + json_file, headers=headers)