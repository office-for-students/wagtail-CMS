# views.py
import requests
from django.http import HttpResponse

API_BASE = "https://search-api-v2-prod-hxhpghhdg3dqdhft.uksouth-01.azurewebsites.net/api/v2/"


def api_proxy(request, path):
    r = requests.get(API_BASE + path, params=request.GET, timeout=10)
    return HttpResponse(r.content, status=r.status_code,
                        content_type=r.headers.get("Content-Type", "application/json"))
