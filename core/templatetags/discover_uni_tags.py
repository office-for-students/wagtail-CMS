import json
import string
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlencode

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from CMS import translations
from CMS.enums import enums
from core.utils import get_code_version, get_current_version, get_language
from courses.models import (
    ACCREDITATION_KEY,
    AFTER_ONE_YEAR_KEY,
    EARNINGS_AFTER_COURSE_KEY,
    EMPLOYMENT_AFTER_COURSE_KEY,
    ENTRY_INFO_KEY,
    GRADUATE_PERCEPTIONS_KEY,
    LINKS_TO_THE_INSTITUTION_WEBSITE_KEY,
    STUDENT_SATISFACTION_KEY,
)

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


@register.simple_tag(takes_context=True)
def nav_is_english(context: Mapping[str, Any]) -> bool:
    """Resolve the nav language even when a view has no CMS page for it."""
    language = context.get('lang')
    if language:
        return bool(language == enums.languages.ENGLISH)

    page = context.get('page')
    if page is not None:
        is_english = page.is_english
        return bool(is_english() if callable(is_english) else is_english)

    request = context.get('request')
    return bool(get_language(getattr(request, 'path', None)) == enums.languages.ENGLISH)


@register.simple_tag
def queryparams(*_, **kwargs):
    safe_args = {key: value for key, value in kwargs.items() if value is not None}
    if safe_args:
        return f'?{urlencode(safe_args)}'
    return ''


@register.simple_tag
def data_not_available(**kwargs):
    language = kwargs.get('language')
    subject = kwargs.get('subject')
    no_data = translations.term_for_key(key="no_data_available", language=language)
    if subject == no_data:
        return "hidden"
    return ""


@register.simple_tag
def get_translation(*_, **kwargs):
    key = kwargs.get('key')
    language = kwargs.get('language')
    term = translations.term_for_key(key, language)
    if 'substitutions' in kwargs:
        term = term % kwargs.get('substitutions')
    return term


@register.simple_tag
def add_line_breaks(*_, **kwargs):
    text = escape(kwargs.get('text', ''))
    text = text.replace('\n\n', '<br /><br />')
    return mark_safe(text)  # noqa: S308 - user text is escaped above; only our <br /> tags are trusted


@register.simple_tag
def split_by_line_break(*_, **kwargs):
    text = kwargs.get('text', '')
    index = kwargs.get('index')
    content = text.split('\n\n')
    try:
        content = content[index]
    except IndexError:
        content = ''
    return content


@register.filter
def is_string(value):
    return isinstance(value, str)


@register.simple_tag
def create_list(*args):
    return args


@register.simple_tag
def insert_values_to_rich_text(*_, **kwargs):
    try:
        return kwargs.get('content').source.format(*kwargs.get('substitutions'))
    except AttributeError:
        kwargs.get('content').format(*kwargs.get('substitutions'))


@register.simple_tag
def length_of_list(view_list):
    return len(view_list)


@register.simple_tag
def map_distance_learning_values(key, language):
    return translations.term_for_key(key, language)


@register.simple_tag
def should_show_accordion(courses, accordion_type):
    if accordion_type == ACCREDITATION_KEY:
        if type(courses) is tuple:
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
def brackets_replace_year(my_string, year):
    if my_string and year:
        return my_string.replace('{}', f'{year}')
    else:
        return ""


@register.simple_tag
def replace_graduate_intro(year):
    if year:
        return year.replace('Students graduating during ', '')
    else:
        return ""


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

    if course.get('title') and course.get('title')['english']:
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
    if locations == [None]:
        print("location is NONE is shouldn't be")
    else:
        if is_english:
            for location in locations:
                if location:
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
    with open("./CMS/static/jsonfiles/regions.json") as f:
        regions = f.read()
    return json.loads(regions)


@register.simple_tag
def concat(*args, **_):
    concat_string = ""
    for arg in args:
        concat_string += str(arg)
    return concat_string


@register.simple_tag
def insert_values_to_plain_text(*_, **kwargs):
    response=kwargs.get('content').format(*kwargs.get('substitutions'))
    return response

@register.simple_tag
def get_salary_from_index(objs: list, index: int):
    try:
        return objs[index]
    except IndexError:
        return objs[0]


@register.simple_tag
def get_item_at_index(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None


@register.simple_tag
def is_franchise(pubukprn, ukprn):
    return pubukprn != ukprn


@register.simple_tag
def format_value(content, substitution):
    return content.replace("{}", str(substitution))


@register.simple_tag
def get_t_number(value, item):
    try:
        t_values = {1: "t1", 2: "t2", 3: "t3", 4: "t4", 5: "t5", 6: "t6", 7: "t7"}
        # Get the corresponding t_value (like t1, t2)
        index = t_values.get(value, "Invalid index")
        # Check if the item has the corresponding attribute
        if index != "Invalid index" and hasattr(item, index):
            t_number = getattr(item, index)
            return str(t_number) if t_number is not None else ""

        return ""
    except Exception:
        return ""


@register.simple_tag
def gcu_course(loop: int, courses: list) -> bool:
    affected_course_id = "11BGLSCI"
    course = courses[loop]
    if course.kis_course_id == affected_course_id:
        return True


@register.simple_tag
def has_theme(courses: list) -> bool:
    return any(course.satisfaction_stats[0].t1 for course in courses)
