from typing import Any
from typing import List
from typing import Tuple

from courses.renderer.sections.base import Section

OVERALL_SATISFACTION = "overall_satisfied"
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
            (self.DATA_FROM_PEOPLE, satisfaction_list[1], "", "satisfaction_stats"),
            (PERCENTAGE_THOSE_ASKED, satisfaction_list[2], "", "satisfaction_stats"),
            (self.DATA_DISPLAYED, "", "", "satisfaction_stats", True)
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
                        suffix=section[suffix_index],
                        multiple=True,
                        unavailable=self.check_unavailable(section)
                    )
                )
        return self.data


class SubSatisfactionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, str, str]]:
        sections = []

        for index, i in enumerate(self.keys):
            if index == 0:
                sections.append((self.DATA_DISPLAYED, "", "", "satisfaction_stats", True))
            sections.append((f"nss_question_{i}", f"question_{i}", "%", "satisfaction_stats"))
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
                        suffix=section[suffix_index],
                        multiple=True,
                        unavailable=self.check_unavailable(section)
                    )
                )

        return self.data
