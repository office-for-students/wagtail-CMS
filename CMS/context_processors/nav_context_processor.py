from django.templatetags.static import static
from wagtail.core.models import Page

from CMS import translations
from CMS.enums import enums
from core.utils import get_language, get_page_for_language


def nav_menu_render(request, url_for_language, menu, footer):
    from courses.models import CourseComparisonPage, CourseManagePage
    from home.models import HomePage
    url = request.get_full_path()
    language = get_language(url)
    search_page_url = get_page_for_language(language, HomePage.objects.all()).url
    comparison_page_url = get_page_for_language(language, CourseComparisonPage.objects.all()).url
    bookmark_page_url = get_page_for_language(language, CourseManagePage.objects.all()).url

    brand_logo = {
        'img': 'images/logos/nav_logo_english.svg', 'url': '/'
    } if language == enums.languages.ENGLISH else {
        'img': 'images/logos/nav_logo_welsh.svg', 'url': '/cy/'
    }
    language_toggle = {'label': 'Cymraeg' if language == enums.languages.ENGLISH else 'English',
                       'sub_items': None,
                       'url': url_for_language}

    return {
        'brand_logo': brand_logo,
        'primary_menu': get_menu(menu, language, 'menu_items') + [language_toggle],
        'comp_menu': [
            {'label': translations.term_for_key(key='search', language=language),
             'img': static('images/search_icon.svg'),
             'url': search_page_url},
            {'label': translations.term_for_key(key='compare', language=language),
             'img': static('images/compare_icon.svg'),
             'url': comparison_page_url},
            {'label': translations.term_for_key(key='saved', language=language),
             'img': static('images/white-bookmark.svg'),
             'url': bookmark_page_url}
        ],
        'footer_menu': get_menu(footer, language, 'footer_items')
    }


def get_menu(model, language, attribute):
    menu = []
    name = enums.languages_map.get(language).capitalize()
    data = model.objects.filter(name=name).first()
    items = getattr(data, attribute)
    for item in items:
        menu.append(parse_menu_item(item))

    return menu


def parse_menu_item(menu_item):
    label = menu_item.value.get('label') if menu_item.value.get('label', '') else menu_item.value.get('link_page').title
    item_dict = {'label': label}
    if 'menu_items' in menu_item.value:
        sub_items = []
        for item in menu_item.value.get('menu_items'):
            sub_items.append(parse_menu_item(item))
        item_dict['sub_items'] = sub_items
    else:
        item_dict['sub_items'] = None
        item_dict['url'] = menu_item.value.get('link_page').url
    return item_dict
