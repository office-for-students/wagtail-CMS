from typing import List, Tuple, Any, Dict

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
    "country",
    "salary_default_country_pop"
]

primary_key = 1
action = 2
prefix_index = 3
model_index = 4


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
                ("1", AVERAGE_EARNINGS, earnings_list[0], "", "go_salaries_inst"),
                ("2", INSTITUTION, earnings_list[1], "£", "go_salaries_inst"),
                ("3", DATA_FROM_PEOPLE, earnings_list[2], "", "go_salaries_inst"),
                ("4", NATIONAL_AVERAGE, earnings_list[3], "£", "go_salaries_sector"),
                ("5", "", earnings_list[4], "", "go_salaries_sector"),
                ("6", DATA_FROM_PEOPLE, earnings_list[5], "", "go_salaries_sector"),

                ("7", AVERAGE_EARNINGS, earnings_list[0], "", "leo3_salaries_inst"),
                ("8", INSTITUTION, earnings_list[1], "£", "leo3_salaries_inst"),
                ("9", DATA_FROM_PEOPLE, earnings_list[2], "", "leo3_salaries_inst"),
                ("10", NATIONAL_AVERAGE, earnings_list[3], "£", "leo3_salaries_sector"),
                ("11", "", earnings_list[4], "", "go_salaries_sector"),
                ("12", DATA_FROM_PEOPLE, earnings_list[5], "", "leo3_salaries_sector"),

                ("13", AVERAGE_EARNINGS, earnings_list[0], "", "leo5_salaries_inst"),
                ("14", INSTITUTION, earnings_list[1], "£", "leo5_salaries_inst"),
                ("15", DATA_FROM_PEOPLE, earnings_list[2], "", "leo5_salaries_inst"),
                ("16", NATIONAL_AVERAGE, earnings_list[3], "£", "leo5_salaries_sector"),
                ("17", "", earnings_list[4], "", "go_salaries_sector"),
                ("18", DATA_FROM_PEOPLE, earnings_list[5], "", "leo5_salaries_sector")
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
            for section in self.sections:
                self.data[section[0]]["values"].append(
                    self.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list=section[model_index],
                        language=self.language,
                        multiple=True,
                        prefix=section[prefix_index]
                    )
                )
        return self.data

    @classmethod
    def multiple_subjects(cls, course: Course, stat: str, model_list: str, language: str, prefix=""):
        response = dict(subject=[], values=[])

        for index, subject in enumerate(course.subject_names):
            subject_name = subject.display_subject_name()
            values = translations.term_for_key(key="no_data_available", language=language)

            if index < len(getattr(course, model_list)):
                _object = getattr(course, model_list)[index]
                method = str(getattr(_object, stat))
                no_data = translations.term_for_key(key="no_data_available", language=language)
                values = f"{prefix}{method}" if method else no_data

            response["subject"].append(subject_name)
            response["values"].append(values)
        return response

    @classmethod
    def presentable_data(cls, course: Course, stat: str, model_list: str, language: str, multiple=False, prefix="") -> str:
        response = translations.term_for_key(key="no_data_available", language=language)
        try:
            if multiple and course.has_multiple_subject_names:
                response = cls.multiple_subjects(
                    course=course,
                    stat=stat,
                    model_list=model_list,
                    language=language,
                    prefix=prefix
                )
            else:
                _object = getattr(course, model_list)[0]
                method = str(getattr(_object, stat))
                if method:
                    response = f"{prefix}{method}" if method.isnumeric() else method
        except Exception as e:
            print("error: ", e)
            pass

        return response
