from typing import Any, Tuple
from typing import Dict
from typing import List

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable_dict import unavailable_dict


def get_subject_unavailable(course: Course, model_list_name: str, language: str, index: int) -> str:
    subject_unavail = None
    subject_names = course.subject_names
    for test in range(len(subject_names)):
        subject_unavail = get_unavailable(course, model_list_name, language, index=index)
    return subject_unavail


def get_unavailable(course: Course, model_list: str, language: str, index: int, accordion=None) -> str:
    response = get_data(
        course=course,
        model_list=model_list,
        language=language,
        accordion=accordion,
        index=index
    )

    return response


def get_data(
        course: Course,
        model_list: str,
        language: str,
        accordion: str,
        index: int
) -> str:
    _object = getattr(course, model_list)[index]
    unavailable_code = str(getattr(_object, "unavailable_code"))
    aggregation_level = str(getattr(_object, "aggregation_level"))
    response_rate = _getattr(_object, "response_rate", None)
    agg = aggregation_level if str(aggregation_level) not in ("None", "") else "blank"
    # Sometimes None was entered into the DB as a string, and sometimes not, sometimes empty string. ^^^
    response = set_message(
        unavailable_key=unavailable_code,
        response_rate=response_rate,
        aggregation_level=agg,
        accordion=accordion,
        language=language
    )

    return response


def set_message(
        unavailable_key: str,
        response_rate: str,
        aggregation_level: str,
        accordion: str,
        language,
) -> str:
    header = translations.term_for_key(key="this_course", language=language)
    override_accordions = [
        translations.term_for_key(key="employment_15_months", language=language),
        translations.term_for_key(key="graduate_perceptions", language=language),
    ]
    if unavailable_key == "None":
        unavailable_key = "2"

    for key, value in unavailable_dict[unavailable_key].items():
        resp = 1 if unavailable_key == "0" and response_rate else 0
        if aggregation_level in key:
            try:
                result = value[resp]
            except IndexError:
                result = value[0]

            title = f"{result}_header"
            header = translations.term_for_key(key=title, language=language)

            if (aggregation_level in ["21", "22", "23", "24"]) and (accordion in override_accordions):
                header = temporary_override(
                    aggregation_level=aggregation_level,
                    language=language
                )

    return header


def _getattr(obj, attr, fallback):
    return getattr(obj, attr) if hasattr(obj, attr) else fallback


#TODO: This is a temporary override. Remove once OFS have stated they want to disable the override.
# Remove accordion from all parameters too. https://app.clickup.com/t/j337mq
def temporary_override(aggregation_level: str, language: str):
    if aggregation_level == "24":
        header = translations.term_for_key(key="this_course", language=language)
        return header
    elif aggregation_level in ["21", "22", "23"]:
        header = translations.term_for_key(key="message_1_header", language=language)
        return header
# end remove
