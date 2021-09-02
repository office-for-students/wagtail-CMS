from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable_dict import unavailable_dict


def get_multiple_subjects(course: Course):
    subjects = list()
    subject_names = course.subject_names
    for subject in subject_names:
        subjects.append(subject.display_subject_name())

    return subjects


def get_unavailable_row(courses: List[Course], model_list: str, language: str, present_as_multiple=False) -> List[Any]:
    columns = []
    for course in courses:
        columns.append(
            get_unavailable(
                course=course,
                model_list=model_list,
                language=language,
                present_as_multiple=present_as_multiple
            )
        )

    return columns


def get_unavailable(course: Course, model_list: str, language: str, present_as_multiple=False) -> Tuple:
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
                data=response,
                subject=subject
            )
    else:
        response = get_data(
            course=course,
            model_list=model_list,
            language=language,
            data=response
        )

    response = response, "The data displayed is from students on"
    print(response)
    return response


def get_data(
        course: Course,
        model_list: str,
        language: str,
        data: Dict[str, List[str]],
        subject=None
) -> Dict[str, List[str]]:
    _object = getattr(course, model_list)[0]
    unavailable_code = str(getattr(_object, "unavailable_code"))
    aggregation_level = str(getattr(_object, "aggregation_level"))
    subject_name = subject or _getattr(_object, "subject_english", "This is a subject")
    response_rate = _getattr(_object, "response_rate", None)
    agg = aggregation_level if str(aggregation_level) not in ("None", "") else "blank"
    # Sometimes None was entered into the DB as a string, and sometimes not, sometimes empty string. ^^^
    response = set_message(unavailable_code, response_rate, agg, subject_name, data, language)

    return response


def set_message(
        unavailable_key: str,
        response_rate: str,
        aggregation_level: str,
        subject: str,
        data: Dict[str, List[str]],
        language,
) -> Dict[str, List[str]]:
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
                message = message.replace("{}", subject) if subject else message.replace("{}", "fix me")
                header = translations.term_for_key(key=title, language=language)

                data["header"].append(header)
                data["message"].append(message)

    except KeyError as ke:
        data["header"].append(f"Fix me {ke}")

    return data


def _getattr(obj, attr, fallback):
    return getattr(obj, attr) if hasattr(obj, attr) else fallback
