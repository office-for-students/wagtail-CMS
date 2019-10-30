import os

import pyclamd

from django.conf import settings

from http import HTTPStatus

from CMS.enums import enums
from core.exceptions import VirusException
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


def check_for_virus(instance):
    if instance.file.closed:
        with open(instance.file.path, 'rb') as file:
            file_content = file.read()
    else:
        file_content = instance.file.read()

    has_virus, name = is_infected(file_content)

    if has_virus:
        raise VirusException(_('Virus "{}" was detected').format(name))

    return instance


def is_infected(stream):
    clam = get_clam()
    if not settings.CLAMAV_ACTIVE or clam is None:
        return None, ''

    result = clam.scan_stream(stream)
    if result:
        return True, result['stream'][1]

    return False, ''


def get_clam():
    try:
        clam = pyclamd.ClamdUnixSocket()

        # test if server is reachable
        clam.ping()

        return clam
    except pyclamd.ConnectionError:
        # if failed, test for network socket
        try:
            cd = pyclamd.ClamdNetworkSocket()
            cd.ping()
            return cd
        except pyclamd.ConnectionError:
            raise ValueError('could not connect to clamd server either by unix or network socket')


def get_version_number():
    with open(os.path.join(settings.BASE_DIR, 'version.txt'), 'r') as file:
        return file.read().replace('\n', '')
