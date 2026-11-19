from django.conf import settings


def environment(request):
    return {"is_production": getattr(settings, "IS_PRODUCTION", False)}
