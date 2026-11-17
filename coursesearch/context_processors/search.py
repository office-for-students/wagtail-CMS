from CMS.settings.base import SEARCH_V2_API


def search_context(request):
    return {"search": {"api_url": SEARCH_V2_API}}
