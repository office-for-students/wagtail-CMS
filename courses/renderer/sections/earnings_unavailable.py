from typing import Any, Tuple
from typing import Dict
from typing import List

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable_dict import earnings_dict


def get_multiple_subjects(course: Course):
    subjects = list()
    subject_names = course.subject_names
    for subject in subject_names:
        subjects.append(subject.display_subject_name())

    return subjects


def get_unavailable(course: Course, model_list: str, language: str) -> Dict[str, List[str]]:
    response = list()

    response = get_data(
        course=course,
        model_list=model_list,
        language=language,
        accordion=accordion,
        data=response,
    )

    return response


def get_data(
        course: Course,
        model_list: str,
        language: str,
        data: List[str],
) -> List[str]:
    _object = getattr(course, model_list)[0]
    unavailable_code = str(getattr(_object, "unavailable_code"))
    aggregation_level = str(getattr(_object, "aggregation_level"))
    kis_level = str(getattr(course, "course_level"))
    is_ni = getattr(_object, "is_ni")
    agg = aggregation_level if str(aggregation_level) not in ("None", "") else "blank"
    # Sometimes None was entered into the DB as a string, and sometimes not, sometimes empty string. ^^^
    response = set_message(
        unavailable_key=unavailable_code,
        aggregation_level=agg,
        kis_level=kis_level,
        is_ni=is_ni,
        data=data,
        language=language
    )
    return response


def set_message(
        unavailable_key: str,
        aggregation_level: str,
        kis_level: str,
        is_ni: bool,
        data: List[str],
        language,
) -> List[str]:
    header = translations.term_for_key(key="this_course", language=language)
    override_accordions = [
        translations.term_for_key(key="employment_15_months", language=language),
        translations.term_for_key(key="graduate_perceptions", language=language),
    ]
    message = earnings_dict[unavailable_key][aggregation_level]

    if not aggregation_level == "blank":
        message = earnings_dict[unavailable_key][aggregation_level][kis_level]

    data.append(message)
    return data


def _getattr(obj, attr, fallback):
    return getattr(obj, attr) if hasattr(obj, attr) else fallback
