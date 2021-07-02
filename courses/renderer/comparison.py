from typing import Callable
from typing import List

from CMS import translations
from CMS.translations import DICT
from courses.models import Course
import logging

logger = logging.getLogger(__name__)

STUDY_MODE = "study_mode"
COURSE_LENGTH = "length"
LOCATIONS = "locations"
DISTANCE_LEARNING = "distance_learning"
PLACEMENT_YEAR = "placement_year"
YEAR_ABROAD = "year_abroad"
FOUNDATION_YEAR = "foundation_year"
PROFESSIONAL_ACCREDITATION = "professional_accreditation"


def dataset_for_comparison_view(courses: List[Course], language="en") -> List[dict]:
    response = []
    context = dict()
    context["course_details"] = dict(
        title=subject_for_key("course_details", language),
        dataset=course_details(courses, language)
    )

    response.append(context)
    return response


def empty_data_structure(key: str, language: str):
    return dict(title=subject_for_key(key, language), values=[])


def course_details(courses: List[Course], language: str):
    primary_key = 0
    action = 1
    sections = [
        (STUDY_MODE, presentable_course_mode),
        (COURSE_LENGTH, presentable_course_length),
        (LOCATIONS, presentable_course_locations),
        (DISTANCE_LEARNING, presentable_distance_learning),
        (PLACEMENT_YEAR, presentable_placement_year),
        (YEAR_ABROAD, presentable_year_abroad),
        (FOUNDATION_YEAR, presentable_foundation_year),
        (PROFESSIONAL_ACCREDITATION, presentable_accreditation)
    ]

    section_1 = dict()
    for section in sections:
        section_1[section[primary_key]] = empty_data_structure(section[primary_key], language)

    for course in courses:
        # Study mode
        # iterate through each required section (see sections = [...] for the course and append the response  to the
        # corresponding (values eg `section["key"]["values"].append` array.
        for section in sections:
            section_1[section[primary_key]]["values"].append(
                section[action](
                    course,
                    language
                )
            )
        # TODO: add next section here

    return section_1


def create_dataset(action: Callable[[Course, str], str], course: Course, language: str):
    return action(course, language)


def subject_for_key(key, language):
    response = DICT.get(key).get(language) if key in DICT else key
    return response


def presentable_course_mode(course, language):
    # Create course mode label as we want it presented in template
    label = course.mode.label
    if label == "Both":
        response = f"{DICT.get('Full-time').get(language)}/{DICT.get('Part-time').get(language)}"
    else:
        response = DICT.get(label).get(language)
    return response


def presentable_course_length(course, language):
    label = course.length.label
    # when switching databases some times this was a string some times it was an int. Remove if data normalised
    number_of_years = label if type(label) == int else int(label.split()[0])

    if number_of_years > 1:
        word_year = translations.DICT["years"].get(language)
    else:
        word_year = translations.DICT["year"].get(language)

    label = f"{number_of_years} {word_year}"
    return label


def presentable_course_locations(course, language=None):
    # all_locations currently determines language inside model due to internal dependency
    # in model class that I don't want to unpick
    return course.all_locations


def presentable_distance_learning(course: Course, language: str):
    if course.distance_learning.code == 1:
        return translations.OPTIONALS['yes'].get(language)
    elif course.distance_learning.code == 0:
        return translations.OPTIONALS["not_available"].get(language)
    else:
        logger.warning("Distance learning code not managed: {course.distance_learning.code}")


def presentable_placement_year(course: Course, language: str):
    code = course.sandwich_year.code
    return string_for_code(code, language, error="Course placement year code not managed:")


def presentable_year_abroad(course: Course, language: str):
    code = course.year_abroad.code
    return string_for_code(code, language, error="Course year abroad code not managed:")


def presentable_foundation_year(course: Course, language: str):
    code = course.foundation_year.code
    return string_for_code(code, language, error="Course Foundations Year code not managed:")


def presentable_accreditation(course: Course, language: str):
    return True if len(course.accreditations) > 0 else False


def string_for_code(code, language, error):
    # called from multiple methods, if one requires a change
    # in terms of the string returned for the code, consider a new method vs editing this one
    if code == 0:
        option = translations.OPTIONALS['not_available']
    elif code == 1:
        option = translations.OPTIONALS['optional']
    elif code == 2:
        option = translations.OPTIONALS['compulsory']
    else:
        logger.warning(f"String for code not available: {code} {error}")
        option = {}

    return option.get(language)
