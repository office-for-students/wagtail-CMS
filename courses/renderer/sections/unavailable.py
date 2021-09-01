from courses.models import Course
from typing import List
from courses.renderer.sections.unavailable_dict import unavailable_dict
from CMS import translations

def get_multiple_subjects(courses: List[Course]):
    subjects = dict(subject=[])
    for course in courses:
        subject_list = list()
        subject_names = course.subject_names
        for subject in subject_names:
            subject_list.append(subject.display_subject_name())
        subjects["subject"].append(subject_list)

    return subjects

def get_unavailable(courses: List[Course], model_list: str, language: str, multiple=False) -> dict:
    data = dict(header=[], message=[])
    for course in courses:
        _object = getattr(course, model_list)[0]
        unavailable_code = str(getattr(_object, "unavailable_code"))
        aggregation_level = str(getattr(_object, "aggregation_level"))
        subject = str(getattr(_object, "subject_english"))
        response_rate = str(getattr(_object, "response_rate"))
        agg = aggregation_level if aggregation_level else "blank"
        print(f"UNAVILBLE CODE: {unavailable_code} \n AGG:{agg} \n resp: {response_rate}")

        set_unavailable(unavailable_code, response_rate, agg, subject, data, language)

    return data


def set_unavailable(unavailable_code, response_rate, agg, subject, data, language):
    try:
        for key, value in unavailable_dict[unavailable_code].items():
            resp = 1 if unavailable_code == "0" and response_rate else 0
            if agg in key:
                result = value[resp]
                title = f"{result}_header"

                message = translations.term_for_key(key=result, language=language)
                message = message.replace("{}", subject)
                header = translations.term_for_key(key=title, language=language)
                print("MESSAGE", result)

                data["header"].append(header)
                data["message"].append(message)
    except KeyError:
        data["header"].append("Fix me")

    return data
