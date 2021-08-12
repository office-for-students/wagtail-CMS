from typing import List, Tuple, Any, Dict
from courses.renderer.sections.base import Section

AVERAGE_EARNINGS = "average_earnings_course_overview_1"
INSTITUTION = "institution"
DATA_FROM_PEOPLE = "data_from_people"
NATIONAL_AVERAGE = "national_average"

earnings_list = [
    "subject_title_in_local_language",
    "med",
    "pop",
    "salary_default_country_med",
    "salary_default_country_pop"
]

primary_key = 1
action = 2
suffix_index = 3
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
            (SHOW_DATA, earnings_list[4], "", f"{prefix}_salaries_sector")
        ]

    def get_sections(self) -> List[Tuple[Any, Any, Any, str]]:
        prefixes = ["go", "leo3", "leo5"]
        sections = [
            (
                ("1", AVERAGE_EARNINGS, earnings_list[0], "", "go_salaries_inst"),
                ("2", INSTITUTION, earnings_list[1], "", "go_salaries_inst"),
                ("3", DATA_FROM_PEOPLE, earnings_list[2], "", "go_salaries_inst"),
                ("4", NATIONAL_AVERAGE, earnings_list[3], "", "go_salaries_sector"),
                ("5", DATA_FROM_PEOPLE, earnings_list[4], "", "go_salaries_sector"),

                ("6", AVERAGE_EARNINGS, earnings_list[0], "", "leo3_salaries_inst"),
                ("7", INSTITUTION, earnings_list[1], "", "leo3_salaries_inst"),
                ("8", DATA_FROM_PEOPLE, earnings_list[2], "", "leo3_salaries_inst"),
                ("9", NATIONAL_AVERAGE, earnings_list[3], "", "leo3_salaries_sector"),
                ("10", DATA_FROM_PEOPLE, earnings_list[4], "", "leo3_salaries_sector"),

                ("11", AVERAGE_EARNINGS, earnings_list[0], "", "leo5_salaries_inst"),
                ("12", INSTITUTION, earnings_list[1], "", "leo5_salaries_inst"),
                ("13", DATA_FROM_PEOPLE, earnings_list[2], "", "leo5_salaries_inst"),
                ("14", NATIONAL_AVERAGE, earnings_list[3], "", "leo5_salaries_sector"),
                ("15", DATA_FROM_PEOPLE, earnings_list[4], "", "leo5_salaries_sector")
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
                        suffix=section[suffix_index]
                    )
                )
        # self.update_data_with_subtitles(self.data)

        return self.data

    # def update_data_with_subtitles(self, data: Dict[str, Any]):
    #     subtitles = {
    #         "5": "unemp_prev_emp_since_grad",
    #         "6": "unemp_not_work_since_grad",
    #         "9": "employed_in_professional",
    #         "10": "employed_not_in_professional",
    #         "11": "employment_type_unknown"
    #     }
    #     for section in self.sections:
    #         if section[0] in subtitles:
    #             data[section[0]]["subtitle"] = self.term_for_key(subtitles[section[0]], self.language)
