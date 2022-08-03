from django.templatetags.static import static

from CMS import translations
from CMS.enums import enums
from core.models import Footer
from core.models import Menu
from core.utils import get_language
from core.utils import get_page_for_language
from courses.models import CourseComparisonPage
from courses.models import CourseManagePage
from home.models import HomePage


def nav_menu_render(request):
    url = request.get_full_path()
    language = get_language(url)
    search_page = get_page_for_language(language, HomePage.objects.all())
    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())

    brand_logo = {
        'img': 'images/logos/nav_logo_english.svg', 'url': '/'
    } if language == enums.languages.ENGLISH else {
        'img': 'images/logos/nav_logo_welsh.svg', 'url': '/cy/'
    }

    return {
        'navigation': {
            'brand_logo': brand_logo,
            'primary_menu': get_menu(Menu, language, 'menu_items'),
            'comp_menu': [
                {'label': translations.term_for_key(key='search', language=language),
                 'img': static('images/search_icon.svg'),
                 'url': search_page.url if search_page else None,
                 'alt': 'Search Page'},
                {'label': translations.term_for_key(key='compare', language=language),
                 'img': static('images/compare_icon.svg'),
                 'url': comparison_page.url if comparison_page else None,
                 'alt': 'Comparison'},

                {'label': translations.term_for_key(key='saved', language=language),
                 'img': static('images/white-bookmark.svg'),
                 'url': bookmark_page.url if bookmark_page else None,
                 'alt': 'Saved',
                 'additional': True}
            ],
            'footer_menu': get_menu(Footer, language, 'footer_items')
        }
    }


def get_menu(model, language, attribute):
    menu = []
    name = enums.languages_map.get(language).capitalize()
    data = model.objects.filter(name=name).first()
    items = getattr(data, attribute) if data else []
    for item in items:
        # TODO: remove when code goes to develop, as added cause we need to used the data and
        #  don't want to edit the CMS just yet - done for show an tell only. Remove the if wrapping statement
        if "Course search" != item.value.get('label') and ("Chwilio am Gwrs") != item.value.get('label'):
            menu.append(parse_menu_item(item))
    return menu


def parse_menu_item(menu_item):
    try:
        label = menu_item.value.get('label') if menu_item.value.get('label') else menu_item.value.get('link_page').title
    except Exception as e:
        print("Menu item has no itle for link page", e)
        label = ""
    item_dict = {'label': label}
    if 'menu_items' in menu_item.value:
        sub_items = []
        for item in menu_item.value.get('menu_items'):
            sub_items.append(parse_menu_item(item))
        item_dict['sub_items'] = sub_items
    else:
        item_dict['sub_items'] = None
        try:
            item_dict['url'] = menu_item.value.get('link_page').url
        except Exception as e:
            print("Menu item has no itle url", e)
            item_dict['url'] = None
    return item_dict
