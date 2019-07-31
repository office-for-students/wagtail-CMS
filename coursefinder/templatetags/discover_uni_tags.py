from urllib.parse import urlencode

from django import template

from CMS.translations import DICT

register = template.Library()


@register.simple_tag
def queryparams(*_, **kwargs):
    safe_args = {key: value for key, value in kwargs.items() if value is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''


@register.simple_tag
def get_translation(*_, **kwargs):
    key = kwargs.get('key')
    language = kwargs.get('language')
    return DICT.get(key).get(language) if key in DICT else ''
