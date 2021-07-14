import logging
from typing import Any, Type
from typing import Callable
from typing import Dict
from typing import List

from CMS import translations

from courses.models import Course
from courses.renderer.sections import CourseDetailSection, SatisfactionSection
from courses.renderer.sections.base import Section

logger = logging.getLogger(__name__)


def dataset_for_comparison_view(courses: List[Course], language="en") -> List[dict]:
    response = []
    context = dict()
    context["course_details"] = dict(
        title=translations.term_for_key(key="course_details", language=language),
        dataset=get_details(CourseDetailSection, courses, language),
        call_to_action=[
            dict(
                show_more=dict(
                    affirmative=translations.term_for_key(key="show_more", language=language),
                    negative=translations.term_for_key(key="show_less", language=language),
                )
            )
        ]
    )

    context["student_satisfaction_course_overview_1"] = dict(
        title=translations.term_for_key(key="student_satisfaction_course_overview_1", language=language),
        dataset=get_details(SatisfactionSection, courses, language),
    )

    response.append(context)
    return response


def get_details(section_model: Type[Section], courses: List[Course], language: str) -> Dict[str, str]:
    section = section_model(courses, language)
    section.prep_data()
    response = section.generate_dict()
    print(f"respone = {response}")
    return response


def create_dataset(action: Callable[[Course, str], str], course: Course, language: str):
    return action(course, language)
