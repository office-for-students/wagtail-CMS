from courses.models import Course
from typing import List, Dict
from courses.renderer.sections.unavailable_dict import unavailable_dict
from CMS import translations


def get_multiple_subjects(course: Course):
    subjects = list()
    subject_names = course.subject_names
    for subject in subject_names:
        subjects.append(subject.display_subject_name())

    return subjects


def get_unavailable(courses: List[Course], model_list: str, language: str, multiple=False) -> dict:
    response = dict(title="The data displayed is from students on", header=[], message=[], multiple={"pk":[], "header":[], "message":[]})
    for course in courses:
        if multiple:
            subjects = get_multiple_subjects(course)
            for index, subject in enumerate(subjects):
                if len(subjects) > 1:
                    response["multiple"]["pk"].append(index)
                response = get_data(course=course, model_list=model_list, language=language, data=response, subject=subject, multiple=len(subjects)>1)
        else:
            response = get_data(course=course, model_list=model_list, language=language, data=response)

    print(response)
    return response


def get_data(course: Course, model_list: str, language: str, data: Dict[str, str], subject=None, multiple=False):
    _object = getattr(course, model_list)[0]
    unavailable_code = str(getattr(_object, "unavailable_code"))
    aggregation_level = str(getattr(_object, "aggregation_level"))
    subject_name = subject or _getattr(_object, "subject_english", "This is a subject")
    response_rate = _getattr(_object, "response_rate", None)
    agg = aggregation_level if str(aggregation_level) not in ("None", "") else "blank"
    # Sometimes None was entered into the DB as a string, and sometimes not, sometimes empty string. ^^^
    response = set_message(unavailable_code, response_rate, agg, subject_name, data, language, multiple=multiple)

    return response


def set_message(unavailable_code, response_rate, agg, subject, data, language, multiple=False):
    try:
        for key, value in unavailable_dict[unavailable_code].items():
            resp = 1 if unavailable_code == "0" and response_rate else 0
            if agg in key:
                try:
                    result = value[resp]
                except IndexError:
                    result = value[0]

                title = f"{result}_header"
                message = translations.term_for_key(key=result, language=language)
                message = message.replace("{}", subject) if subject else message.replace("{}", "fix me")
                header = translations.term_for_key(key=title, language=language)
                if multiple:
                    data["multiple"]["header"].append(header)
                    data["multiple"]["message"].append(message)
                else:
                    data["header"].append(header)
                    data["message"].append(message)
                details = (
                    f"UNAVILBLE CODE: {unavailable_code} \n AGG:{agg} \n resp: {response_rate}, \n SUBJECT: {subject} \n {result}")
    except KeyError:
        data["header"].append("Fix me")

    return data


def _getattr(obj, attr, fallback):
    return getattr(obj, attr) if hasattr(obj, attr) else fallback
