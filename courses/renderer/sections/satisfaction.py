from typing import List, Tuple, Any

from courses.models import Course
from courses.renderer.sections.base import Section

OVERALL_SATISFACTION = "overall_satisfied"
SATISFACTION_DATA_FROM_PEOPLE = "data_from_people"
PERCENTAGE_THOSE_ASKED = "percent_of_those_asked"

satisfaction_list = [
    "question_27",
    "number_of_students",
    "response_rate",
]

primary_key = 0
action = 1
suffix_index = 2
model_array = 3


class SatisfactionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, Any, Any]]:
        sections = [
            (OVERALL_SATISFACTION, satisfaction_list[0], "%", "satisfaction_stats"),
            (SATISFACTION_DATA_FROM_PEOPLE, satisfaction_list[1], "", "satisfaction_stats"),
            (PERCENTAGE_THOSE_ASKED, satisfaction_list[2], "", "satisfaction_stats")
        ]

        return sections

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.sections:
                self.data[section[primary_key]]["values"].append(
                    self.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list=section[model_array],
                        language=self.language,
                        suffix=section[suffix_index]
                    )
                )

        return self.data


class SubSatisfactionSection(Section):

    def __init__(self, keys: List[str], courses, language='en'):
        self.keys = keys
        super().__init__(courses, language)

    def get_sections(self) -> List[Tuple[Any, Any, str, str]]:
        sections = []

        for i in self.keys:
            sections.append((f"nss_question_{i}", f"question_{i}", "%", "satisfaction_stats"))
        return sections

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.sections:
                self.data[section[primary_key]]["values"].append(
                    self.__class__.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list=section[model_array],
                        language=self.language,
                        suffix=section[suffix_index]
                    )
                )

        return self.data
