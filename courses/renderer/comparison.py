import logging
from typing import Callable
from typing import Dict
from typing import List
from typing import Type

from CMS import translations
from courses.models import Course
from courses.renderer.sections import CourseDetailSection
from courses.renderer.sections import SatisfactionSection
from courses.renderer.sections.base import Section
from courses.renderer.sections.continuation import ContinuationSection
from courses.renderer.sections.employment import SubEmploymentSection
from courses.renderer.sections.graduate_perception import GraduatePerceptionSection
from courses.renderer.sections.satisfaction import SubSatisfactionSection

logger = logging.getLogger(__name__)


def get_accordion_dataset(title: str, dataset, call_to_action=[]):
    response = dict(
        title=title,
        dataset=dataset,
        call_to_action=call_to_action
    )

    return response


def get_sub_satisfaction(language) -> List:
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
    return list_sub_accordions


def get_sub_employment(language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="employment_after_the_course", language=language), [0, 7]),
        (translations.term_for_key(key="occupation_type", language=language), [7, 11]),
    ]
    return list_sub_accordions


def get_sub_accordion_dataset(courses, section_model, get_sub_headers, language) -> List:
    response = []

    for accordion in get_sub_headers(language):
        response.append(
            dict(
                title=accordion[0],
                dataset=get_details(
                    **dict(
                        section_model=section_model,
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
            guidance_information=(
                translations.term_for_key(key="satisfaction_guidance_1", language=language),
                translations.term_for_key(key="satisfaction_guidance_2", language=language)
            ),
            dataset=get_details(SatisfactionSection, courses, language),
            sub_accordions=get_sub_accordion_dataset(courses, SubSatisfactionSection, get_sub_satisfaction, language),
            change_point=4,
            source=(
                translations.term_for_key(key="about_our_data_link", language=language),
                translations.term_for_key(key="read_more_about_satisfaction", language=language)
            )
        ),
        # TODO: Update with correct data when you get to that ticket
        # dict(
        #     title=translations.term_for_key(key="entry_information", language=language),
        #     guidance_information=(translations.term_for_key(key="entry_guidance", language=language),),
        #     source=(
        #         translations.term_for_key(key="about_our_data_link", language=language),
        #         translations.term_for_key(key="read_more_about_entry", language=language)
        #     )
        # ),
        # End
        dict(
            title=translations.term_for_key(key="after_one_year", language=language),
            guidance_information=(translations.term_for_key(key="after_one_year_guidance", language=language),),
            dataset=get_details(ContinuationSection, courses, language),
            source=(
                translations.term_for_key(key="entrance_data_read_more_url", language=language),
                translations.term_for_key(key="read_more_about_continuation", language=language),
            )
        ),
        # TODO: Update with correct data when you get to that ticket
        dict(
            title=translations.term_for_key(key="earnings_after_the_course", language=language),
            guidance_information=(
                translations.term_for_key(key="earnings_guidance_1", language=language),
                translations.term_for_key(key="earnings_guidance_2", language=language),
                translations.term_for_key(key="earnings_guidance_3", language=language)
            ),
            source=(
                translations.term_for_key(key="earnings_link", language=language),
                translations.term_for_key(key="read_more_about_earnings", language=language),
            )
        ),
        dict(
            title=translations.term_for_key(key="employment_15_months", language=language),
            guidance_information=(
                translations.term_for_key(key="employment_guidance_1", language=language),
                translations.term_for_key(key="employment_guidance_2", language=language),
                translations.term_for_key(key="employment_guidance_3", language=language)
            ),
            sub_accordions=get_sub_accordion_dataset(courses, SubEmploymentSection, get_sub_employment, language),
            source=(
                translations.term_for_key(key="earnings_link", language=language),
                translations.term_for_key(key="read_more_about_employment", language=language),
            )
        ),
        dict(
            title=translations.term_for_key(key="graduate_perceptions", language=language),
            guidance_information=(
                translations.term_for_key(key="graduate_guidance_1", language=language),
                translations.term_for_key(key="graduate_guidance_2", language=language),
            ),
            dataset=get_details(GraduatePerceptionSection, courses, language),
            source=(
                translations.term_for_key(key="graduate_link", language=language),
                translations.term_for_key(key="read_more_about_graduate_perceptions", language=language),
            )
        ),
        # dict(
        #     title=translations.term_for_key(key="information_on_uni", language=language),
        # ),
        # end
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
