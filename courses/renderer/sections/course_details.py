from typing import List, Tuple, Any

from CMS import translations
from courses.models import Course
from courses.renderer.sections.base import Section
import logging

STUDY_MODE = "study_mode"
COURSE_LENGTH = "length"
LOCATIONS = "locations"
DISTANCE_LEARNING = "distance_learning"
PLACEMENT_YEAR = "placement_year"
YEAR_ABROAD = "year_abroad"
FOUNDATION_YEAR = "foundation_year"
PROFESSIONAL_ACCREDITATION = "professional_accreditation"

primary_key = 0
action = 1

logger = logging.getLogger(__name__)


def presentable_course_mode(course: Course, language: str) -> str:
    # Create course mode label as we want it presented in template
    if course:
        label = course.mode.label
        if label == "Both":
            response = f"{translations.term_for_key('Full-time', language=language)}/{translations.term_for_key('Part-time', language=language)}"
        else:
            response = translations.term_for_key(label, language=language)
        return response
    return None


def presentable_course_length(course: Course, language: str) -> str:
    if course:
        label = course.length.label
        # when switching databases some times this was a string some times it was an int. Remove if data normalised
        number_of_years = label if type(label) == int else int(label.split()[0])

        if number_of_years > 1:
            word_year = translations.term_for_key(key="years", language=language)
        else:
            word_year = translations.term_for_key(key="year", language=language)

        label = f"{number_of_years} {word_year}" if not number_of_years == 0 else ""
        return label
    return None


def presentable_course_locations(course: Course, language=None) -> str:
    # all_location_names currently determines language inside model due to internal dependency
    # in model class that I don't want to unpick
    if course:
        response = ""
        for index, location in enumerate(course.all_location_names):
            display = index + 1
            response += f"{display}. {location} <br/>"

        return response
    return None


def presentable_distance_learning(course: Course, language: str) -> str:
    if course:
        if int(course.distance_learning.code) == 1:
            return translations.term_for_key(key='yes', language=language)
        elif int(course.distance_learning.code) == 0:
            return translations.term_for_key(key="not_available", language=language)
        else:
            return translations.term_for_key(key="optional", language=language)
    return None


def presentable_placement_year(course: Course, language: str) -> str:
    if course:
        code = course.sandwich_year.code
        return string_for_code(code, language, error="Course placement year code not managed:")
    return None


def presentable_year_abroad(course: Course, language: str) -> str:
    if course:
        code = course.year_abroad.code
        return string_for_code(code, language, error="Course year abroad code not managed:")
    return None


def presentable_foundation_year(course: Course, language: str) -> str:
    if course:
        code = course.foundation_year.code
        return string_for_code(code, language, error="Course Foundations Year code not managed:")
    return None


def presentable_accreditation(course: Course, language: str) -> str:
    if course:
        value = True if len(course.accreditations) > 0 else False
        none_text = translations.term_for_key(key='none_recorded', language=language)

        if value:
            return '<i class="fas fa-check-circle course_comparison-table__tick-icon"></i>'
        else:
            return f"-<br/>{none_text}"
    return None

def string_for_code(code: int, language: str, error: str) -> str:
    # called from multiple methods, if one requires a change
    # in terms of the string returned for the code, consider a new method vs editing this one
    if code == 0:
        option = translations.term_for_key(key='not_available', language=language)
    elif code == 1:
        option = translations.term_for_key(key='optional', language=language)
    elif code == 2:
        option = translations.term_for_key(key='compulsory', language=language)
    else:
        logger.warning(f"String for code not available: {code} {error}")
        option = {}

    return option


class CourseDetailSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any]]:
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
        return sections

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.sections:
                self.data[section[primary_key]]["values"].append(
                    section[action](
                        course,
                        self.language
                    )
                )
        return self.data
