import logging

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

_session = requests.Session()

FORWARD_REQUEST_HEADERS = ("Content-Type", "Accept", "Accept-Language")
FORWARD_RESPONSE_HEADERS = ("Content-Type", "Cache-Control", "ETag", "Last-Modified")

MAX_BODY_BYTES = 1 * 1024 * 1024  # 1 MB; reject anything larger

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_proxy(request, path):
    if ".." in path or path.startswith("/"):
        return JsonResponse({"error": "Invalid path"}, status=400)

    base = settings.SEARCH_API_BASE_URL.rstrip("/") + "/"
    upstream_url = base + path

    headers = {h: request.headers[h] for h in FORWARD_REQUEST_HEADERS if h in request.headers}

    body = None
    if request.method == "POST":
        if len(request.body) > MAX_BODY_BYTES:
            return JsonResponse({"error": "Request body too large"}, status=413)
        body = request.body

    try:
        upstream = _session.request(
            method=request.method,
            url=upstream_url,
            params=request.GET,
            data=body,
            headers=headers,
            timeout=getattr(settings, "SEARCH_API_TIMEOUT", 10),
            allow_redirects=False,
        )
    except requests.Timeout:
        logger.warning("Search API timed out: %s %s", request.method, upstream_url)
        return JsonResponse({"error": "Upstream timed out"}, status=504)
    except requests.RequestException:
        logger.exception("Search API request failed: %s %s", request.method, upstream_url)
        return JsonResponse({"error": "Upstream unavailable"}, status=502)

    response = HttpResponse(upstream.content, status=upstream.status_code)
    for h in FORWARD_RESPONSE_HEADERS:
        if h in upstream.headers:
            response[h] = upstream.headers[h]

    return response