from core.utils import get_language
from .translations import term_for_key

def comp_menu_renderer(request):
    language = get_language(request.get_full_path())
    search = term_for_key(key='search', language=language)
    compare = term_for_key(key='compare', language=language)
    saved = term_for_key(key='saved', language=language)
    return {
        'comp_menu': [{'label': search, 'img': 'images/search_icon.svg'},
                         {'label': compare, 'img': 'images/search_icon.svg'},
                         {'label': saved, 'img': 'images/white-bookmark.svg'}],
    }
