from typing import List, Tuple, Any, Dict

from django.template.loader import render_to_string

from CMS import translations
from courses.models import Course
from courses.renderer.sections.base import Section

AVERAGE_EARNINGS = "average_earnings_course_overview_1"
INSTITUTION = "institution"
DATA_FROM_PEOPLE = "data_from_people"
NATIONAL_AVERAGE = "national_average"
REGION = "regions"

earnings_list = [
    "subject_title_in_local_language",
    "med",
    "pop",
    "salary_default_country_med",
    "salary_default_country_pop"
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

    def subs(self, prefix):
        return [
            (AVERAGE_EARNINGS, earnings_list[0], "", f"{prefix}_salaries_inst"),
            (INSTITUTION, earnings_list[1], "", f"{prefix}_salaries_inst"),
            (DATA_FROM_PEOPLE, earnings_list[2], "", f"{prefix}_salaries_inst"),
            (NATIONAL_AVERAGE, earnings_list[3], "", f"{prefix}_salaries_sector"),
            # (SHOW_DATA, earnings_list[4], "", f"{prefix}_salaries_sector")
        ]

    def get_sections(self) -> List[Tuple[Any, Any, Any, str]]:
        prefixes = ["go", "leo3", "leo5"]
        sections = [
            (
                ("1", AVERAGE_EARNINGS, earnings_list[0], "", "go_salaries_inst", "first"),
                ("2", INSTITUTION, earnings_list[1], "£", "go_salaries_inst", False),
                ("3", DATA_FROM_PEOPLE, earnings_list[2], "", "go_salaries_inst", False),
                ("4", NATIONAL_AVERAGE, earnings_list[3], "£", "go_salaries_sector", False),
                ("6", DATA_FROM_PEOPLE, earnings_list[4], "", "go_salaries_sector", "final"),

                ("7", AVERAGE_EARNINGS, earnings_list[0], "", "leo3_salaries_inst", "first"),
                ("8", INSTITUTION, earnings_list[1], "£", "leo3_salaries_inst", False),
                ("9", DATA_FROM_PEOPLE, earnings_list[2], "", "leo3_salaries_inst", False),
                ("10", NATIONAL_AVERAGE, earnings_list[3], "£", "leo3_salaries_sector", False),
                ("12", DATA_FROM_PEOPLE, earnings_list[4], "", "leo3_salaries_sector", "final"),

                ("13", AVERAGE_EARNINGS, earnings_list[0], "", "leo5_salaries_inst", "first"),
                ("14", INSTITUTION, earnings_list[1], "£", "leo5_salaries_inst", False),
                ("15", DATA_FROM_PEOPLE, earnings_list[2], "", "leo5_salaries_inst", False),
                ("16", NATIONAL_AVERAGE, earnings_list[3], "£", "leo5_salaries_sector", False),
                ("18", DATA_FROM_PEOPLE, earnings_list[4], "", "leo5_salaries_sector", "final")
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
                        model_list=section[model_index],
                        language=self.language,
                        prefix=section[prefix_index],
                        extra=section[extras]
                    )
                )
        return self.data

    @classmethod
    def multiple_subjects(cls, course: Course, stat: str, model_list: str, language: str, prefix="", extra=False):
        response = dict(subject=[], values=[])

        for index, subject in enumerate(course.subject_names):
            subject_name = subject.display_subject_name()
            values = "no_data"

            if index < len(getattr(course, model_list)):
                _object = getattr(course, model_list)[index]
                method = str(getattr(_object, stat))

                if extra == "first":
                    mode = translations.term_for_key(course.mode.label, language=language)
                    values = f'{mode} {method} {translations.term_for_key("course", language=language)}' if method else values
                elif extra == "final":
                    country = str(getattr(_object, "country"))
                    values = render_to_string(
                        "courses/partials/country_population.html",
                        context=dict(
                            country=country,
                            population=method
                        )
                    ) if method else values
                else:
                    values = f"{prefix}{method}" if method else values

            response["subject"].append(subject_name)
            response["values"].append(values)
        return response

    @classmethod
    def presentable_data(cls, course: Course, stat: str, model_list: str, language: str, prefix="", extra=False) -> str:
        response = "no_data"
        try:
            if course.has_multiple_subject_names:
                response = cls.multiple_subjects(
                    course=course,
                    stat=stat,
                    model_list=model_list,
                    language=language,
                    prefix=prefix,
                    extra=extra
                )
            else:
                _object = getattr(course, model_list)[0]
                method = str(getattr(_object, stat))
                mode = translations.term_for_key(course.mode.label, language=language)

                if extra == "first":
                    response = f'{mode} {method} {translations.term_for_key("course", language=language)}' if method else response
                elif extra == "final":
                    country = str(getattr(_object, "country"))
                    response = render_to_string(
                        "courses/partials/country_population.html",
                        context=dict(
                            country=country,
                            population=method
                        )
                    ) if method else response
                else:
                    response = f"{prefix}{method}" if method else response

        except Exception as e:
            print("error: ", e)
            pass

        return response
