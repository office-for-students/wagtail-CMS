import logging
from typing import Any, Type, Callable, Dict, List, Tuple

from CMS import translations

from courses.models import Course
from courses.renderer.sections import CourseDetailSection, SatisfactionSection
from courses.renderer.sections.base import Section
from courses.renderer.sections.satisfaction import SubSatisfactionSection

logger = logging.getLogger(__name__)


def get_accordion_dataset(title: str, dataset, call_to_action=[]):
    response = dict(
        title=title,
        dataset=dataset,
        call_to_action=call_to_action
    )

    return response


def get_sub_accordion_dataset(courses, language):
    list_sub_accordions = [
        (translations.term_for_key(key="teaching_on_my_course", language=language), [4, 5, 6, 7]),
        (translations.term_for_key(key="learning_opportunities", language=language), [8, 9, 10]),
        (translations.term_for_key(key="assessment_and_feedback", language=language), [11, 12, 13, 14]),
        (translations.term_for_key(key="academic_support", language=language), [15, 16, 17]),
        (translations.term_for_key(key="organisation_and_management",
                                   language=language), [18, 19, 20]),
        (translations.term_for_key(key="learning_resources", language=language), [21, 22, 23]),
        (translations.term_for_key(key="learning_community", language=language), [24, 25]),
        (translations.term_for_key(key="student_voice", language=language), [26, 27, 28, 29])
    ]
    response = []

    for accordion in list_sub_accordions:

        response.append(dict(
            title=accordion[0],
            dataset=SubSatisfactionSection(
                keys=accordion[1],
                courses=courses,
                language=language
            )
        ))

    return response


def dataset_for_comparison_view(courses: List[Course], language="en") -> List[dict]:
    response = []
    context = dict()
    context["course_details"] = get_accordion_dataset(
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
        sub_accordions=get_sub_accordion_dataset(courses, language)
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
