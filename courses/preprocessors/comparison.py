from typing import List

from CMS import translations
from CMS.translations import DICT
from courses.models import Course


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
    number_of_years = label if type(label) == int else int(label.split()[0])
    if language == "en":
        if number_of_years > 1:
            word_year = "years"
        else:
            word_year = "year"
    else:
        if number_of_years > 1:
            word_year = "mlynedd"
        else:
            word_year = "blynedd"

    label = f"{number_of_years} {word_year}"
    return label


def presentable_distance_learning(course: Course, language: str):
    if course.distance_learning.code:
        return "Yes" if language == "en" else "Ydy"
    else:
        return "Not available" if language == "en" else "Ddim ar gael"


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
    if code == 0:
        return "Not available" if language == "en" else "Ddim ar gael"
    elif code == 1:
        return "Optional" if language == "en" else "Dewisol"
    elif code == 3:
        return "Compulsory" if language == "en" else "Gorfodol"
    else:
        raise Exception(f"{error} {code}")


def subject_for_key(key, language):
    response = DICT.get(key).get(language) if key in DICT else key
    return response


def dict_for_comparison_view_for_courses(courses: List[Course], language="en") -> List[dict]:
    response = []
    context = dict()
    context["Course Details"] = course_details(courses, language)
    response.append(context)
    return response


def course_details(courses: List[Course], language: str):
    items = []

    STUDY_MODE = "study_mode"
    COURSE_LENGTH = "length"
    LOCATIONS = "locations"
    DISTANCE_LEARNING = "distance_learning"
    PLACEMENT_YEAR = "placement_year"
    YEAR_ABROAD = "year_abroad"
    FOUNDATION_YEAR = "foundation_year"
    PROFESSIONAL_ACCREDITATION = "professional_accreditation"

    section_1 = dict()
    section_1[subject_for_key(STUDY_MODE, language)] = []
    section_1[subject_for_key(COURSE_LENGTH, language)] = []
    section_1[subject_for_key(LOCATIONS, language)] = []
    section_1[subject_for_key(DISTANCE_LEARNING, language)] = []
    section_1[subject_for_key(PLACEMENT_YEAR, language)] = []
    section_1[subject_for_key(YEAR_ABROAD, language)] = []
    section_1[subject_for_key(FOUNDATION_YEAR, language)] = []
    section_1[subject_for_key(PROFESSIONAL_ACCREDITATION, language)] = []

    for course in courses:
        # Study mode
        section_1[subject_for_key(STUDY_MODE, language)].append(presentable_course_mode(
            course,
            language
        ))

        # Course length
        section_1[subject_for_key(COURSE_LENGTH, language)].append(presentable_course_length(
            course,
            language
        ))

        # Course locations
        section_1[subject_for_key(LOCATIONS, language)].append(course.all_locations)

        # Distance Learning
        section_1[subject_for_key(DISTANCE_LEARNING, language)].append(
            presentable_distance_learning(
                course,
                language
            )
        )

        # Placement Year
        section_1[subject_for_key(PLACEMENT_YEAR, language)].append(
            presentable_placement_year(
                course,
                language
            )
        )
        print(f"course.sandwich_year: {course.sandwich_year.code}")
        # Year abroad
        section_1[subject_for_key(YEAR_ABROAD, language)].append(
            presentable_year_abroad(
                course, language
            )
        )
        #
        # # Foundation year
        section_1[subject_for_key(FOUNDATION_YEAR, language)].append(
            presentable_foundation_year(
                course,
                language
            )
        )
        # Professional Accreditation
        section_1[subject_for_key(PROFESSIONAL_ACCREDITATION, language)].append(
            presentable_accreditation(
                course,
                language
            )
        )

        items.append(section_1)
    print(section_1)

    return items
