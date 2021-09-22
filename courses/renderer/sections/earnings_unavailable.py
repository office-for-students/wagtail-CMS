from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable_dict import earnings_dict


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
    unavailable_code = getattr(_object, "unavail_reason")
    aggregation_level = _getattr(_object, "aggregate", "blank")
    kis_level = getattr(course, "course_level")
    is_ni = _getattr(_object, "is_ni", False)

    return set_message(
        unavailable_key=str(unavailable_code),
        aggregation_level=aggregation_level,
        kis_level=str(kis_level),
        language=language
    )


def set_message(
        unavailable_key: str,
        aggregation_level: str,
        kis_level: str,
        language: str
) -> str:
    message = earnings_dict[unavailable_key]["blank"]
    message = translations.term_for_key(key=message, language=language)

    if not aggregation_level == "blank":
        message = earnings_dict[unavailable_key][aggregation_level].get(kis_level)
        message = translations.term_for_key(key=message, language=language)

    return message


def _getattr(obj, attr, fallback):
    return getattr(obj, attr) if hasattr(obj, attr) else fallback
