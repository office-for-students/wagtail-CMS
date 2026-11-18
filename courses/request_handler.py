import hashlib
import json
from threading import local
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache
from requests.adapters import HTTPAdapter

from core.request_handler import REQUEST_TIMEOUT

_SESSION_LOCAL = local()
DEFAULT_COURSE_DATA_CACHE_SECONDS = 600


def _get_session() -> requests.Session:
    session = getattr(_SESSION_LOCAL, "session", None)
    if session is None:
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        _SESSION_LOCAL.session = session
    return session


def _course_data_cache_key(institution_id: str, course_id: str, mode: int | None) -> str:
    identity = json.dumps([institution_id, course_id, mode], separators=(",", ":"))
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    return f"courses:course_data:{digest}"


def load_course_data(
    institution_id: str, course_id: str, mode: int | None
) -> dict[str, Any] | requests.Response:
    """Reuse pooled connections and cached course data to avoid repeated upstream latency."""
    cache_seconds = getattr(settings, "COURSE_DATA_CACHE_SECONDS", DEFAULT_COURSE_DATA_CACHE_SECONDS)
    cache_key = _course_data_cache_key(institution_id, course_id, mode)
    if cache_seconds > 0:
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

    headers = {
        'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
    }
    base_url = "%s/institutions/%s/courses/%s/modes/%s"

    response = _get_session().get(
        url=base_url % (settings.DATASETAPIHOST, institution_id, course_id, mode),
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    if 200 <= response.status_code < 300:
        course_data = response.json()
        if isinstance(course_data, dict):
            if cache_seconds > 0:
                cache.set(cache_key, course_data, cache_seconds)
            return course_data
    return response