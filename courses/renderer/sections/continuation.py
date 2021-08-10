from typing import List, Tuple, Any

from courses.models import Course
from courses.renderer.sections.base import Section

CONTINUATION_DATA_FROM_PEOPLE = "data_from_people"
STILL_STUDYING = "still_on_course"
TAKING_BREAK = "break_from_studies"
LEFT_WITH_LOWER = "left_lower_qualification"
LEFT_WITHOUT_QUALIFICATION = "left_no_qualification"

continuation_list = [
    "number_of_students",
    "continuing",
    "dormant",
    "lower",
    "left",
]

primary_key = 0
action = 1
suffix_index = 2
model_array = 3


def presentable_continuation(course: Course, stat: str, suffix: Any, language: str) -> str:
    if language == 'cy':
        response = "Nid yw'r data ar gael"
    else:
        response = "No data available"
    try:
        _object = course.continuation_stats[0]
        method = str(getattr(_object, stat))
        response = f"{method}{suffix}" if suffix and method.isnumeric() else method
    except Exception as e:
        print("error: ", e)
        pass

    return response


class ContinuationSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, str, str]]:
        sections = [
            (CONTINUATION_DATA_FROM_PEOPLE, continuation_list[0], "", "continuation_stats"),
            (STILL_STUDYING, continuation_list[1], "%", "continuation_stats"),
            (TAKING_BREAK, continuation_list[2], "%", "continuation_stats"),
            (LEFT_WITH_LOWER, continuation_list[3], "%", "continuation_stats"),
            (LEFT_WITHOUT_QUALIFICATION, continuation_list[4], "%", "continuation_stats")
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
