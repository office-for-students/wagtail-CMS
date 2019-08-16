from urllib.parse import urlencode

from django import template

from CMS.enums import enums
from CMS.translations import DICT
from content.models import Section
from courses.models import STUDENT_SATISFACTION_KEY, ENTRY_INFO_KEY, AFTER_ONE_YEAR_KEY, AFTER_COURSE_KEY, \
    ACCREDITATION_KEY

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
    string = DICT.get(key).get(language) if key in DICT else ''

    if not string:
        string = DICT.get(key).get(enums.languages.ENGLISH) if key in DICT else ''

    if 'substitutions' in kwargs:
        string = string % kwargs.get('substitutions')
    return string


@register.simple_tag
def create_list(*args):
    return args


@register.simple_tag
def insert_values_to_rich_text(*_, **kwargs):
    list(kwargs.get('substitutions'))
    return kwargs.get('content').source % (kwargs.get('substitutions'))


@register.simple_tag
def length_of_list(view_list):
    return len(view_list)


@register.simple_tag
def map_distance_learning_values(key, language):
    if key in DICT.get('distance_learning_values'):
        return DICT.get('distance_learning_values').get(key).get(language)
    return key


@register.simple_tag
def should_show_accordion(course, accordion_type):
    if accordion_type == STUDENT_SATISFACTION_KEY:
        return course.show_satisfaction_stats
    elif accordion_type == ACCREDITATION_KEY:
        return course.accreditations
    elif accordion_type == ENTRY_INFO_KEY:
        return course.show_entry_information_stats
    # TODO implement specific checks for other accordions
    return True
