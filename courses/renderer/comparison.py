import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type

from CMS import translations
from courses.models import Course
from .sections import CourseDetailSection
from .sections import SatisfactionSection
from .sections.base import Section
from .sections.continuation import ContinuationSection
from .sections.earnings import SubEarningsSection
from .sections.employment import SubEmploymentSection
from .sections.entry import SubEntrySection
from .sections.graduate_perception import GraduatePerceptionSection
from .sections.information import InformationSection
from .sections.satisfaction import SubSatisfactionSection
from .sections.unavailable import get_subject_unavailable

logger = logging.getLogger(__name__)


def get_accordion_dataset(title: str, dataset, call_to_action=List[Dict[Any, Dict[Any, str]]]):
    response = dict(
        title=title,
        dataset=dataset,
        call_to_action=call_to_action
    )

    return response


def get_sub_satisfaction(language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="teaching", language=language), [1, 2, 3, 4]),
        (translations.term_for_key(key="learning_opportunities", language=language), [5, 6, 7, 8, 9]),
        (translations.term_for_key(key="assessment_and_feedback", language=language), [10, 11, 12, 13, 14]),
        (translations.term_for_key(key="academic_support", language=language), [15, 16]),
        (translations.term_for_key(key="organisation_and_management",
                                   language=language), [17, 18]),
        (translations.term_for_key(key="learning_resources", language=language), [19, 20, 21]),
        (translations.term_for_key(key="student_voice", language=language), [22, 23, 24, 25]),
        (translations.term_for_key(key="mental_wellbeing", language=language), [26]),
        (translations.term_for_key(key="freedom_of_expression", language=language), [27]),
    ]
    return list_sub_accordions

def get_sub_overall_satisfaction(language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="teaching", language=language), translations.term_for_key(key='overall_teaching_on_my_course', language=language)),
        (translations.term_for_key(key="learning_opportunities", language=language), translations.term_for_key(key='overall_learning_opportunities', language=language)),
        (translations.term_for_key(key="assessment_and_feedback", language=language), translations.term_for_key(key='overall_assessment_and_feedback', language=language)),
        (translations.term_for_key(key="academic_support", language=language), translations.term_for_key(key='overall_academic_support', language=language)),
        (translations.term_for_key(key="organisation_and_management", language=language), translations.term_for_key(key='overall_organisation_and_management', language=language)),
        (translations.term_for_key(key="learning_resources", language=language), translations.term_for_key(key='overall_learning_resources', language=language)),
        (translations.term_for_key(key="student_voice", language=language), translations.term_for_key(key='overall_student_voice', language=language)),
    ]
    return list_sub_accordions


def get_sub_employment(language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="employment_after_the_course", language=language), [0, 9]),
        (translations.term_for_key(key="occupation_type", language=language), [9, 15]),
    ]
    return list_sub_accordions


def get_sub_earnings(language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="after_15_months", language=language), [0, 6]),
        (translations.term_for_key(key="after_3_years", language=language), [6, 11]),
        (translations.term_for_key(key="after_5_years", language=language), [11, 16]),
    ]
    return list_sub_accordions


def get_sub_entry(language) -> List:
    list_sub_accordions = [
        (translations.term_for_key(key="qualification_types", language=language), [0, 10]),
        (translations.term_for_key(key="ucas_tariff_points", language=language), [10, 13]),
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


def get_multiple_subjects(courses: List[Course], sources: List[str], language, earnings=False, override=False) -> Dict[str, List[str]]:
    subjects = dict(subject=[])
    for course in courses:
        subject_list = list()
        subject_names = course.subject_names

        for index, subject_name in enumerate(subject_names):
            subject = get_subject_label(course, index, sources, language, earnings, subject_names)
            no_data_available = translations.term_for_key(key="no_data_available", language=language)
            # TODO: remove when the override is to be disabled
            #  + remove override parameter from this function and graduate and employment context
            if override:
                subject = override_replace(subject, language)
            # End remove
            if not subject == no_data_available:
                subject_list.append(subject)

        subjects["subject"].append(subject_list)
    return subjects


def override_replace(sub, language):
    if sub == translations.term_for_key(key="message_2_header", language=language):
        return translations.term_for_key(key="this_course", language=language)
    if sub == translations.term_for_key(key="message_3_header", language=language):
        return translations.term_for_key(key="message_4_header", language=language)
    return sub


def has_valid_value(attrib, _object):
    method = getattr(_object, attrib)
    if method is not None:
        return True

    return False


def get_subject_label(course, index, sources, language, earnings, subject_names):
    no_data_available = translations.term_for_key(key="no_data_available", language=language)
    fallback = no_data_available
    attrib = "display_subject_name"
    for source in sources:
        try:
            if not earnings:
                fallback = get_subject_unavailable(course, source, language, index)
                if len(subject_names) == 1 and fallback == no_data_available:
                    fallback = translations.term_for_key(key="this_course", language=language)
            _object = getattr(course, f'{source}')[index]

        except IndexError as e:
            continue

        if earnings:
            attrib = "subject_title_in_local_language"
        if has_valid_value(
                _object=_object,
                attrib=attrib
        ):
            if not earnings and getattr(_object, attrib)() is None:
                return fallback
            else:
                return getattr(_object, attrib)

    return fallback


def dataset_for_comparison_view(courses: List[Course], language="en") -> List[dict]:
    response = []
    context = dict()
    context["course_details"] = get_accordion_dataset(
        title=translations.term_for_key(key="course_details", language=language),
        dataset=get_details(CourseDetailSection, courses, language),
        call_to_action=[
            dict(
                show_more=dict(
                    affirmative=translations.term_for_key(key="expand", language=language),
                    negative=translations.term_for_key(key="minimise", language=language),
                )
            )
        ]
    )
    context["no_data"] = [translations.term_for_key(key="no_data_available", language=language),
                          translations.term_for_key(key="unavailable_data_message", language=language)]
    context["accordions"] = [
        dict(
            title=translations.term_for_key(key="student_satisfaction_course_overview_1", language=language),
            guidance_information=(
                translations.term_for_key(key="satisfaction_guidance_1", language=language),
                translations.term_for_key(key="satisfaction_guidance_2", language=language)
            ),
            subjects=get_multiple_subjects(courses, ["satisfaction_stats"], language=language),
            dataset=get_details(SatisfactionSection, courses, language),
            sub_accordions=get_sub_accordion_dataset(courses, SubSatisfactionSection, get_sub_satisfaction, language),
            overall_sub_accordions=get_sub_overall_satisfaction(language),
            change_point=4,
            source=(
                translations.term_for_key(key="about_our_data_link", language=language),
                translations.term_for_key(key="read_more_about_satisfaction", language=language)
            )
        ),
        dict(
            title=translations.term_for_key(key="entry_information", language=language),
            guidance_information=(translations.term_for_key(key="entry_guidance", language=language),),
            multi_subject_selectors=[get_multiple_subjects(courses, ["entry_stats"], language=language),
                                     get_multiple_subjects(courses, ["tariff_stats"], language=language)],
            sub_accordions=get_sub_accordion_dataset(courses, SubEntrySection, get_sub_entry, language),
            source=(
                translations.term_for_key(key="about_our_data_link", language=language),
                translations.term_for_key(key="read_more_about_entry", language=language)
            )
        ),
        dict(
            title=translations.term_for_key(key="after_one_year", language=language),
            guidance_information=(translations.term_for_key(key="after_one_year_guidance", language=language),),
            subjects=get_multiple_subjects(courses, ["continuation_stats"], language=language),
            dataset=get_details(ContinuationSection, courses, language),
            source=(
                translations.term_for_key(key="entrance_data_read_more_url", language=language),
                translations.term_for_key(key="read_more_about_continuation", language=language),
            )
        ),
        dict(
            title=translations.term_for_key(key="earnings_after_the_course", language=language),
            guidance_information=(
                translations.term_for_key(key="earnings_guidance_1", language=language),
                translations.term_for_key(key="earnings_guidance_2", language=language),
                translations.term_for_key(key="earnings_guidance_3", language=language)
            ),
            subjects=get_multiple_subjects(courses, ["go_salaries_inst", "leo3_salaries_inst", "leo5_salaries_inst"],
                                           language=language, earnings=True),
            sub_accordions=get_sub_accordion_dataset(courses, SubEarningsSection, get_sub_earnings, language),
            source=(
                translations.term_for_key(key="earnings_link", language=language),
                translations.term_for_key(key="read_more_about_earnings", language=language),
            ),
            earnings=True
        ),
        dict(
            title=translations.term_for_key(key="employment_15_months", language=language),
            guidance_information=(
                translations.term_for_key(key="employment_guidance_1", language=language),
                translations.term_for_key(key="employment_guidance_2", language=language),
                translations.term_for_key(key="employment_guidance_3", language=language)
            ),
            multi_subject_selectors=[get_multiple_subjects(courses, ["employment_stats"], language=language, override=True),
                                     get_multiple_subjects(courses, ["job_type_stats"], language=language, override=True)],
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
            subjects=get_multiple_subjects(courses, ["graduate_perceptions"], language=language, override=True),
            dataset=get_details(GraduatePerceptionSection, courses, language),
            source=(
                translations.term_for_key(key="graduate_link", language=language),
                translations.term_for_key(key="read_more_about_graduate_perceptions", language=language),
            )
        ),
        dict(
            title=translations.term_for_key(key="information_on_uni", language=language),
            dataset=get_details(InformationSection, courses, language)
        ),

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
