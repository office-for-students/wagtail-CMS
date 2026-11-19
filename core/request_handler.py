import os
from typing import cast

import requests
from django.conf import settings

# (connect, read) seconds; stops a slow upstream from hanging a request worker indefinitely.
REQUEST_TIMEOUT = (3.05, 10)


def send_feedback(feedback_data):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }

    return requests.post(
        url=settings.FEEDBACK_API_HOST, headers=headers, data=feedback_data, timeout=REQUEST_TIMEOUT
    )


def get_json_file(json_file: str) -> requests.Response:
    if settings.LOCAL == "True" or settings.JSONFILES_STORAGE_CONTAINER == "" or json_file == "subjects.json":
        with open(os.path.join(settings.BASE_DIR, 'CMS/static/jsonfiles/' + json_file)) as file:
            data = file.read()
            response = requests.Response()

            response_state = response.__getstate__()
            response_state["status_code"] = 200
            response_state["_content"] = data.encode('utf-8')
            response_state["encoding"] = 'utf-8'

            response.__setstate__(response_state)

            return response
    else:
        container_url = cast(str, os.getenv('JSONFILES_STORAGE_CONTAINER'))
        return requests.get(container_url + "/" + json_file, timeout=REQUEST_TIMEOUT)


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
        path = settings.JSONFILES_STORAGE_CONTAINER + "/" + "sitemaps.xml"
        response = requests.get(path, timeout=REQUEST_TIMEOUT)
        return response


def is_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
