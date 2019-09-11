from django.shortcuts import render
from django.views.static import serve

from core.utils import get_page_for_language
from home.models import HomePage


def holding_page(request, language='en'):
    page = get_page_for_language(language, HomePage.objects.all())
    context = {
        'page': page,
    }

    if '/cy/' in request.path:
        return render(request, 'home/welsh_holding.html', context)
    return render(request, 'home/english_holding.html', context)


def statics(request, path):
    if 'scss' in path:
        path = 'css/' + path
    return serve(request, path, document_root='./CMS/static/')
