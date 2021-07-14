from typing import List, Tuple, Any

from courses.models import Course
from courses.renderer.sections.base import Section

OVERALL_SATISFACTION = "overall_satisfied"
SATISFACTION_DATA_FROM_PEOPLE = "data_from_people"
PERCENTAGE_THOSE_ASKED = "percent_of_those_asked"

satisfaction_list = [
    "question_27.agree_or_strongly_agree",
    "number_of_students",
    "response_rate"
]

primary_key = 0
action = 1


def presentable_satisfaction(course: Course, stat: str, language: str) -> str:
    response = "No data available"
    try:
        _object = course.satisfaction_stats[0]
        method = getattr(_object, stat)
        response = method
        print(f"{stat} data= {response}")
    except Exception as e:
        print("error: ", e)
        pass

    return response


class SatisfactionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any]]:
        self.sections = [
            (OVERALL_SATISFACTION, satisfaction_list[0]),
            (SATISFACTION_DATA_FROM_PEOPLE, satisfaction_list[1]),
            (PERCENTAGE_THOSE_ASKED, satisfaction_list[2])
        ]
        return self.sections

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.get_sections():
                self.data[section[primary_key]]["values"].append(
                    presentable_satisfaction(course, section[action], self.language)
                )

        return self.data
