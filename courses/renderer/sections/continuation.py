from typing import Any
from typing import List
from typing import Tuple

from courses.renderer.sections.base import Section

CONTINUATION_DATA_FROM_PEOPLE = "data_from_people"
STILL_STUDYING = "still_on_course"
LEFT_WITH_LOWER = "left_lower_qualification"
LEFT_WITHOUT_QUALIFICATION = "left_no_qualification"

continuation_list = [
    "number_of_students",
    "continuing",
    "lower",
    "left",
]

primary_key = 0
action = 1
suffix_index = 2
model_array = 3
unavailable = 4


class ContinuationSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, str, str]]:
        sections = [
            (self.DATA_DISPLAYED, "", "", "continuation_stats", True),
            (CONTINUATION_DATA_FROM_PEOPLE, continuation_list[0], "", "continuation_stats"),
            (STILL_STUDYING, continuation_list[1], "%", "continuation_stats"),
            (LEFT_WITH_LOWER, continuation_list[2], "%", "continuation_stats"),
            (LEFT_WITHOUT_QUALIFICATION, continuation_list[3], "%", "continuation_stats")
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
                        unavailable=self.check_unavailable(section),
                        multiple=True
                    )
                )
        return self.data

