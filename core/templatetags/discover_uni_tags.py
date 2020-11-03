import string
import json

from urllib.parse import urlencode

from django import template

from CMS.enums import enums
from CMS.translations import DICT
from core.utils import get_current_version, get_code_version

from django.utils.safestring import mark_safe
from wagtail.core.rich_text import RichText, expand_db_html


from courses.models import STUDENT_SATISFACTION_KEY, ENTRY_INFO_KEY, AFTER_ONE_YEAR_KEY, ACCREDITATION_KEY,\
    EARNINGS_AFTER_COURSE_KEY, EMPLOYMENT_AFTER_COURSE_KEY, GRADUATE_PERCEPTIONS_KEY, LINKS_TO_THE_INSTITUTION_WEBSITE_KEY

register = template.Library()

SHOW_STATS_LOOKUP = {
    STUDENT_SATISFACTION_KEY: 'show_satisfaction_stats',
    ENTRY_INFO_KEY: 'show_entry_information_stats',
    AFTER_ONE_YEAR_KEY: 'show_after_one_year_stats',
    ACCREDITATION_KEY: 'accreditations',
    EARNINGS_AFTER_COURSE_KEY: 'show_after_course_stats',
    EMPLOYMENT_AFTER_COURSE_KEY: 'show_employment_after_course_stats',
    GRADUATE_PERCEPTIONS_KEY: 'show_graduate_perceptions_stats',
    LINKS_TO_THE_INSTITUTION_WEBSITE_KEY: 'show_links_to_the_institution_website'
}


@register.simple_tag
def current_version():
    return get_current_version()


@register.simple_tag
def code_version():
    return get_code_version()


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
    string = DICT.get(key).get(language) if key in DICT else key

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
    return kwargs.get('content').source.format(*kwargs.get('substitutions'))


@register.simple_tag
def length_of_list(view_list):
    return len(view_list)


@register.simple_tag
def map_distance_learning_values(key, language):
    if key in DICT.get('distance_learning_values'):
        return DICT.get('distance_learning_values').get(key).get(language)
    return key


@register.simple_tag
def should_show_accordion(courses, accordion_type):
    if accordion_type == ACCREDITATION_KEY:
        if type(courses) == tuple:
            show = False
            for course in courses:
                if course and course.accreditations:
                    show = True
            return show
        return courses.accreditations
    return True


@register.simple_tag
def title_to_id(title):
    return title.replace(' ', '_').lower()


@register.simple_tag
def get_alphabet():
    return list(string.ascii_lowercase)


@register.simple_tag
def get_max_length(list1, list2):
    return max(len(list1), len(list2))


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag
def get_index(index, view_list):
    if len(view_list) > index:
        return view_list[index]
    return None


@register.simple_tag
def get_course_name(course, is_english):
    name = ''
    if course.get('qualification'):
        name += course.get('qualification') + ' '
    if course.get('honours_award') and course.get('honours_award') == 1:
        name += '(Hons) '
    title = course.get('title')
    if title and is_english:
        name += title.get('english') if title.get('english') else title.get('welsh')
    else:
        name += title.get('welsh') if title.get('welsh') else title.get('english')
    return name


@register.simple_tag
def get_course_locations_list(locations, is_english):
    locations_list = []
    if is_english:
        for location in locations:
            location_name = location.get('english') if location.get('english') else location.get('welsh')
            locations_list.append(location_name)
    else:
        for location in locations:
            location_name = location.get('welsh') if location.get('welsh') else location.get('english')
            locations_list.append(location_name)
    return ','.join(locations_list)


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def is_multiple_of(number, base):
    return number % base == 0


@register.simple_tag
def get_index_of_item(item, view_list):
    return view_list.index(item)


@register.simple_tag
def get_region_list():
    with open("./CMS/static/jsonfiles/regions.json", "r") as f:
        regions = f.read()
    return json.loads(regions)


@register.simple_tag
def concat(*args, **_):
    concat_string = ""
    for arg in args:
        concat_string += str(arg)
    return concat_string

# @register.simple_tag
# def get_prov_pc_verb(value, data_source):
#     value2 = value.deepcopy()
#     if data_source == "go":
#         value2.source = value2.source.replace("based", "fish")
#     else:
#         value2.source = value2.source.replace("employed", "based")
#     return value2

@register.simple_tag
def insert_values_to_plain_text(*_, **kwargs):
    return kwargs.get('content').format(*kwargs.get('substitutions'))