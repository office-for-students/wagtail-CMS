import logging
from typing import Any, Type, Callable, Dict, List, Tuple

from CMS import translations

from courses.models import Course
from courses.renderer.sections import CourseDetailSection, SatisfactionSection
from courses.renderer.sections.base import Section
from courses.renderer.sections.continuation import ContinuationSection
from courses.renderer.sections.satisfaction import SubSatisfactionSection

logger = logging.getLogger(__name__)


def get_accordion_dataset(title: str, dataset, call_to_action=[]):
    response = dict(
        title=title,
        dataset=dataset,
        call_to_action=call_to_action
    )

    return response


def get_sub_accordion_dataset(courses, language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="teaching_on_my_course", language=language), [1, 2, 3, 4]),
        (translations.term_for_key(key="learning_opportunities", language=language), [5, 6, 7]),
        (translations.term_for_key(key="assessment_and_feedback", language=language), [8, 9, 10, 11]),
        (translations.term_for_key(key="academic_support", language=language), [12, 13, 14]),
        (translations.term_for_key(key="organisation_and_management",
                                   language=language), [15, 16, 17]),
        (translations.term_for_key(key="learning_resources", language=language), [18, 19, 20]),
        (translations.term_for_key(key="learning_community", language=language), [21, 22]),
        (translations.term_for_key(key="student_voice", language=language), [23, 24, 25, 26])
    ]
    response = []

    for accordion in list_sub_accordions:
        response.append(
            dict(
                title=accordion[0],
                dataset=get_details(
                    **dict(
                        section_model=SubSatisfactionSection,
                        courses=courses,
                        language=language,
                        keys=accordion[1]
                    )
                )
            )
        )

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

    context["accordions"] = [
        dict(
            title=translations.term_for_key(key="student_satisfaction_course_overview_1", language=language),
            dataset=get_details(SatisfactionSection, courses, language),
            sub_accordions=get_sub_accordion_dataset(courses, language),
            change_point=4,
            source=(1,
                    translations.term_for_key(key="about_our_data_link", language=language),
                    translations.term_for_key(key="national_student_survey", language=language)
                    )
        ),
        dict(
            title=translations.term_for_key(key="after_one_year", language=language),
            dataset=get_details(ContinuationSection, courses, language),
            source=(6,
                    translations.term_for_key(key="entrance_data_read_more_url", language=language),
                    translations.term_for_key(key="data_ind_stud_coll_dir", language=language)
                    )
        )
        #TODO: additional accordions to be added here, however, in the order they are supposed to appear.
    ]

    response.append(context)
    return response


def get_details(section_model: Type[Section], courses: List[Course], language: str, keys=None) -> Dict[str, str]:
    if keys:
        section = section_model(courses=courses, language=language, keys=keys)
    else:
        section = section_model(courses=courses, language=language)

    section.prep_data()
    response = section.generate_dict()
    return response


def create_dataset(action: Callable[[Course, str], str], course: Course, language: str):
    return action(course, language)
