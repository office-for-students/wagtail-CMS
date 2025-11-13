# api/api.py
from ninja import NinjaAPI
from wagtail.models import Page

api = NinjaAPI(title="Wagtail API", version="1.0.0")


@api.get("/pages")
def list_pages(request):
    pages = Page.objects.live().public().values("id", "title", "slug")
    return list(pages)
