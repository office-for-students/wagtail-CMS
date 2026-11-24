from typing import Any

from django.conf import settings
from django.http import HttpRequest


def environment(request: HttpRequest) -> dict[str, Any]:
    return {
        "is_production": getattr(settings, "IS_PRODUCTION", False),
        "google_analytics_id": getattr(settings, "GOOGLE_ANALYTICS_ID", ""),
    }
