from typing import Any
from typing import List
from typing import Tuple

from django.template.loader import render_to_string

from CMS import translations
from courses.models import Course
from courses.renderer.sections.base import Section
from courses.renderer.sections.earnings_unavailable import get_unavailable

AVERAGE_EARNINGS = "average_earnings_course_overview_1"
INSTITUTION = "this_institution"
DATA_FROM_PEOPLE = "data_from_people"
NATIONAL_AVERAGE = "national_average"
REGION = "regions"
PERCENTAGE_THOSE_ASKED = "percent_of_those_asked"

earnings_list = [
    "subject_title_in_local_language",
    "med",
    "pop",
    "salary_default_country_med",
    "salary_default_country_pop",
    "resp_rate"
]

primary_key = 1
action = 2
prefix_index = 3
model_index = 4
extras = 5


class SubEarningsSection(Section):

    def __init__(self, keys: List, courses, language='en'):
        self.start_range = keys[0]
        self.end_range = keys[1]
        super().__init__(courses, language)

    def get_sections(self) -> List[Tuple[Any, Any, Any, str]]:
        sections = [
            (
                ("1", AVERAGE_EARNINGS, earnings_list[0], "", "go_salaries_inst", "first"),
                ("2", INSTITUTION, earnings_list[1], "£", "go_salaries_inst", False),
                ("3", DATA_FROM_PEOPLE, earnings_list[2], "", "go_salaries_inst", "institution"),
                ("4", PERCENTAGE_THOSE_ASKED, earnings_list[5], "", "go_salaries_inst", False),
                ("5", NATIONAL_AVERAGE, earnings_list[3], "£", "go_salaries_sector", "national"),
                ("6", DATA_FROM_PEOPLE, earnings_list[4], "", "go_salaries_sector", "final"),

                ("7", AVERAGE_EARNINGS, earnings_list[0], "", "leo3_salaries_inst", "first"),
                ("8", INSTITUTION, earnings_list[1], "£", "leo3_salaries_inst", False),
                ("9", DATA_FROM_PEOPLE, earnings_list[2], "", "leo3_salaries_inst", "institution"),
                ("10", NATIONAL_AVERAGE, earnings_list[3], "£", "leo3_salaries_sector", "national"),
                ("11", DATA_FROM_PEOPLE, earnings_list[4], "", "leo3_salaries_sector", "final"),

                ("12", AVERAGE_EARNINGS, earnings_list[0], "", "leo5_salaries_inst", "first"),
                ("13", INSTITUTION, earnings_list[1], "£", "leo5_salaries_inst", False),
                ("14", DATA_FROM_PEOPLE, earnings_list[2], "", "leo5_salaries_inst", "institution"),
                ("15", NATIONAL_AVERAGE, earnings_list[3], "£", "leo5_salaries_sector", "national"),
                ("16", DATA_FROM_PEOPLE, earnings_list[4], "", "leo5_salaries_sector", "final")
            )
        ]
        sub_sections = []

        for i in range(self.start_range, self.end_range):
            sub_sections.append((sections[0][i]))

        return sub_sections

    def prep_data(self):
        self.data = {}
        self.sections = self.get_sections()
        for section in self.sections:
            self.data[section[0]] = self.empty_data_structure(section[primary_key], self.language)

    def generate_dict(self) -> dict:
        for course in self.courses:
            for index, section in enumerate(self.sections):
                self.data[section[0]]["values"].append(
                    self.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list_name=section[model_index],
                        language=self.language,
                        prefix=section[prefix_index],
                        extra=section[extras]
                    )
                )
        return self.data

    @classmethod
    def multiple_subjects(cls, course: Course, stat: str, model_list_name: str, language: str, prefix="", extra=False):
        response = dict(subject=[], values=[])
        no_data = translations.term_for_key(key="no_data_available", language=language)

        for index, subject in enumerate(course.subject_names):
            subject_name = subject.display_subject_name()
            values = cls.set_unavailable(
                course=course,
                model_list_name=model_list_name,
                language=language,
                extra=extra
            )

            if index < len(getattr(course, model_list_name)):
                _object = getattr(course, model_list_name)[index]
                method = getattr(_object, stat)

                if extra == "first":
                    mode = translations.term_for_key(course.mode.label, language=language)
                    course_string = f'{mode} {method} {translations.term_for_key("course", language=language)}' if method else values
                    header = course_string if method else translations.term_for_key(key="no_data_available",
                                                                                    language=language)
                    values = cls.set_unavailable(
                        course=course,
                        model_list_name=model_list_name,
                        language=language,
                        extra=extra,
                        header=header
                    )
                elif extra == "institution":
                    institution = course.institution_name
                    values = render_to_string(
                        "courses/partials/institution_snippet.html",
                        context=dict(
                            additional_field=institution,
                            field=f"{prefix}{method}"
                        )
                    ) if method else values
                elif extra == "final":
                    country = getattr(_object, "country")
                    values = render_to_string(
                        "courses/partials/country_population.html",
                        context=dict(
                            additional_field=country,
                            field=method
                        )
                    ) if method else values
                else:
                    values = f"{prefix}{method}" if method else values

            response["values"].append(values)
            response["subject"].append(subject_name)
        return response

    @classmethod
    def presentable_data(
            cls,
            course: Course,
            stat: str,
            model_list_name: str,
            language: str,
            multiple=False,
            prefix="",
            extra=False
    ) -> str:
        response = cls.set_unavailable(
            course=course,
            model_list_name=model_list_name,
            language=language,
            extra=extra
        )
        no_data = translations.term_for_key(key="no_data_available", language=language)
        try:
            if course.has_multiple_subject_names:
                response = cls.multiple_subjects(
                    course=course,
                    stat=stat,
                    model_list_name=model_list_name,
                    language=language,
                    prefix=prefix,
                    extra=extra
                )
            else:
                _object = getattr(course, model_list_name)[0]
                method = getattr(_object, stat)
                mode = translations.term_for_key(course.mode.label, language=language)

                if extra == "first":
                    course_string = f'{mode} {method} {translations.term_for_key("course", language=language)}'
                    header = course_string if method else no_data
                    response = cls.set_unavailable(
                        course=course,
                        model_list_name=model_list_name,
                        language=language,
                        extra=extra,
                        header=header
                    )
                elif extra == "institution":
                    institution = course.institution_name
                    response = render_to_string(
                        "courses/partials/institution_snippet.html",
                        context=dict(
                            additional_field=institution,
                            field=f"{prefix}{method}"
                        )
                    ) if method else response
                elif extra == "final":
                    country = getattr(_object, "country")
                    response = render_to_string(
                        "courses/partials/country_population.html",
                        context=dict(
                            additional_field=country,
                            field=method
                        )
                    ) if method else response
                else:
                    response = f"{prefix}{method}" if method else response

        except Exception as e:
            # print("error: ", e)
            pass

        return response

    @classmethod
    def set_unavailable(cls, course: Course, model_list_name: str, language: str, extra=False, header=None):
        if extra == "first":
            header = header
            body = get_unavailable(course=course, model_list_name=model_list_name, language=language, first=True)
            if course.is_ni_provider and "go" not in model_list_name:
                body = translations.term_for_key(key="unavailable_northern_ireland", language=language)
        else:
            if course.is_ni_provider and "go" not in model_list_name:
                body = translations.term_for_key(key="unavailable_northern_ireland", language=language)
            else:
                _object = getattr(course, model_list_name)[0] if "sector" not in model_list_name else None
                method = getattr(_object, "unavailable_body") if _object else None
                header = translations.term_for_key(key="no_data_available", language=language)
                body = method

        if extra == "final" or extra == "national":
            header = translations.term_for_key(key="no_data_available", language=language)
            return ["unavailable", header]

        if header is None:
            header = translations.term_for_key(key="no_data_available", language=language)

        if body is not None:
            return ["unavailable", header, body]
        else:
            return header