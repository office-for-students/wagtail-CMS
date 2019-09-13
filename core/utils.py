from http import HTTPStatus

from CMS.enums import enums
from errors.models import InternalError


def get_page_for_language(language, pages):

    def is_correct_language(page):
        return page.get_language() == language

    page_for_language = list(filter(is_correct_language, pages))

    if not page_for_language and language == enums.languages.ENGLISH:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR,
                      'Bad configuration - No page of this type for the required language')
        return None

    if not page_for_language:
        fallback_page = get_page_for_language(enums.languages.ENGLISH, pages)
        if fallback_page:
            InternalError(HTTPStatus.INTERNAL_SERVER_ERROR,
                          'Bad configuration - No page of this type for the required language, '
                          'falling back to English version')
        else:
            InternalError(HTTPStatus.INTERNAL_SERVER_ERROR,
                          'Bad configuration - No page of this type for the required language, no fallback found')
        return fallback_page

    if len(page_for_language) > 1:
        InternalError(HTTPStatus.INTERNAL_SERVER_ERROR,
                      'Bad configuration - Found multiple copies of this page type for this language')
    return page_for_language[0]


def parse_menu_item(menu_item):
    label = menu_item.value.get('label') if menu_item.value.get('label') else menu_item.value.get('link_page').title
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


def fallback_to(value, default_value):
    return value if value is not None else default_value
