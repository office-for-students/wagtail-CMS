from typing import Any, Tuple
from typing import Dict
from typing import List

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable_dict import unavailable_dict


def get_multiple_subjects(course: Course):
    subjects = list()
    subject_names = course.subject_names
    for subject in subject_names:
        subjects.append(subject.display_subject_name())

    return subjects


def get_unavailable_rows(courses: List[Course], model_list: List[str], language: str, change_key=0,
                         present_as_multiple=False) -> Tuple:
    columns = []
    title = translations.term_for_key(key="data_displayed", language=language)

    for index, course in enumerate(courses):
        columns.append(
            get_unavailable(
                course=course,
                model_list=model_list[1] if change_key > index else model_list[0],
                language=language,
                present_as_multiple=present_as_multiple
            )
        )

    return columns, title


def get_unavailable(course: Course, model_list: str, language: str, accordion=None, present_as_multiple=False) -> Dict[str, List[str]]:
    response = dict(
        header=[],
        message=[],
    )

    if present_as_multiple:
        subjects = get_multiple_subjects(course)
        for index, subject in enumerate(subjects):
            response = get_data(
                course=course,
                model_list=model_list,
                language=language,
                accordion=accordion,
                data=response,
                subject=subject
            )
    else:
        subject = get_multiple_subjects(course)[0]
        response = get_data(
            course=course,
            model_list=model_list,
            language=language,
            accordion=accordion,
            data=response,
            subject=subject
        )

    response = response
    return response


def get_data(
        course: Course,
        model_list: str,
        language: str,
        data: Dict[str, List[str]],
        accordion: str,
        subject=None
) -> Dict[str, List[str]]:
    _object = getattr(course, model_list)[0]
    unavailable_code = str(getattr(_object, "unavailable_code"))
    aggregation_level = str(getattr(_object, "aggregation_level"))
    response_rate = _getattr(_object, "response_rate", None)
    agg = aggregation_level if str(aggregation_level) not in ("None", "") else "blank"
    # Sometimes None was entered into the DB as a string, and sometimes not, sometimes empty string. ^^^
    response = set_message(
        unavailable_key=unavailable_code,
        response_rate=response_rate,
        aggregation_level=agg,
        subject=subject,
        accordion=accordion,
        data=data,
        language=language
    )

    return response


def set_message(
        unavailable_key: str,
        response_rate: str,
        aggregation_level: str,
        subject: str,
        accordion: str,
        data: Dict[str, List[str]],
        language,
) -> Dict[str, List[str]]:
    header = translations.term_for_key(key="this_course", language=language)
    override_accordions = [
        translations.term_for_key(key="employment_15_months", language=language),
        translations.term_for_key(key="graduate_perceptions", language=language),
    ]
    try:
        for key, value in unavailable_dict[unavailable_key].items():
            resp = 1 if unavailable_key == "0" and response_rate else 0
            if aggregation_level in key:
                try:
                    result = value[resp]
                except IndexError:
                    result = value[0]

                title = f"{result}_header"
                message = translations.term_for_key(key=result, language=language)
                message = message.replace("{}", subject) if subject else message.replace("{}", "")
                header = translations.term_for_key(key=title, language=language)

                if (aggregation_level in ["21", "22", "23", "24"]) and (accordion in override_accordions):
                    header = temporary_override(
                        aggregation_level=aggregation_level,
                        language=language
                    )

                data["header"].append(header)
                data["message"].append(message)

    except KeyError:
        data["header"].append(header)
    return data


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
