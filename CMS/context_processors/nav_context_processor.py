from CMS import translations
from CMS.enums import enums
from core.models import Menu, Footer
from core.utils import get_language, get_page_for_language
from courses.models import CourseComparisonPage, CourseManagePage


def nav_menu_render(request):
    url = request.get_full_path()
    language = get_language(url)
    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())
    search = translations.term_for_key(key='search', language=language)
    compare = translations.term_for_key(key='compare', language=language)
    saved = translations.term_for_key(key='saved', language=language)
    brand_logo = {'img': 'images/logos/nav_logo_english.svg', 'url': '/'} if language == 'en' else {
        'img': 'images/logos/nav_logo_welsh.svg', 'url': 'cy/'}

    # TODO: Add comparison image below
    return {
        'navigation': {
            'brand_logo': brand_logo,
            'primary_menu': get_menu(Menu, language, 'menu_items'),
            'comp_menu': [{'label': search, 'img': 'images/search_icon.svg', 'url': '/'},
                          {'label': compare, 'img': 'images/search_icon.svg', 'url': comparison_page.url},
                          {'label': saved, 'img': 'images/white-bookmark.svg', 'url': bookmark_page.url}],
            'footer_menu': get_menu(Footer, language, 'footer_items')
        }
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
