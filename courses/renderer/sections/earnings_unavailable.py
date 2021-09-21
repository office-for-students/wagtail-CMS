from typing import Any, Tuple
from typing import Dict
from typing import List

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable_dict import earnings_first_dict


def get_unavailable(course: Course, model_list_name: str, language: str, first=False) -> str:
    response = get_data(
        course=course,
        model_list_name=model_list_name,
        language=language
    )
    return response


def get_data(
        course: Course,
        model_list_name: str,
        language: str
) -> str:
    _object = getattr(course, model_list_name)[0]
    unavailable_code = str(getattr(_object, "unavail_reason"))
    print("Unavailable code: ", unavailable_code)
    aggregation_level = _getattr(_object, "aggregate", "blank")
    kis_level = str(getattr(course, "course_level"))
    is_ni = _getattr(_object, "is_ni", False)
    response = set_message(
        unavailable_key=unavailable_code,
        aggregation_level=aggregation_level,
        kis_level=kis_level,
        is_ni=is_ni,
        language=language
    )
    return response


def set_message(
        unavailable_key: str,
        aggregation_level: str,
        kis_level: str,
        is_ni: bool,
        language: str
) -> str:
    message = earnings_dict[unavailable_key]["blank"]
    message = translations.term_for_key(key=message, language=language)

    if not aggregation_level == "blank":
        message = earnings_dict[unavailable_key][aggregation_level].get(kis_level)
        message = translations.term_for_key(key=message, language=language)
    if is_ni:
        message = translations.term_for_key(key="unavailable_northern_ireland", language=language)

    return message


def _getattr(obj, attr, fallback):
    return getattr(obj, attr) if hasattr(obj, attr) else fallback
