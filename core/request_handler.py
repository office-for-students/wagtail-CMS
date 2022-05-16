import os

import requests
from django.conf import settings


def send_feedback(feedback_data):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.post(url=settings.FEEDBACK_API_HOST, headers=headers, data=feedback_data)


def get_json_file(json_file):
    if settings.LOCAL == "True" or settings.JSONFILES_STORAGE_CONTAINER == "" or json_file == "subjects.json":
        with open(os.path.join(settings.BASE_DIR, 'CMS/static/jsonfiles/' + json_file)) as json_file:
            data = json_file.read()
            response = requests.Response()

            response_state = response.__getstate__()
            response_state["status_code"] = 200
            response_state["_content"] = data.encode('utf-8')
            response_state["encoding"] = 'utf-8'

            response.__setstate__(response_state)

            return response
    else:
        return requests.get(os.getenv('JSONFILES_STORAGE_CONTAINER') + "/" + json_file)


def get_sitemap_file():
    if settings.LOCAL == "True" or settings.JSONFILES_STORAGE_CONTAINER == "":
        response = requests.Response()

        response_state = response.__getstate__()
        response_state["status_code"] = 200
        response_state["_content"] = "<xml></xml>"
        response_state["encoding"] = 'utf-8'
        response_state["content_type"] = "text/xml"
        response.__setstate__(response_state)

        return response
    else:
        return requests.get(settings.JSONFILES_STORAGE_CONTAINER + "/" + settings.SITEMAP_STORAGE_BLOB)
