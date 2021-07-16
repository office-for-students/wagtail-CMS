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


def presentable_satisfaction(course: Course, stat: str, language: str) -> str:
    response = "No data available"
    print(f"state = {stat}")
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


class SubSatisfactionSection(Section):

    def __init__(self, keys: List[str], courses, language='en'):
        self.keys = keys
        super().__init__(courses, language)

    def get_sections(self) -> List[Tuple[Any, Any]]:
        for i in self.keys:
            print("i ", i)
            self.sections.append((f"nss_question_{i}", f"question_{i}"))

        return self.sections

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.get_sections():
                self.data[section[primary_key]]["values"].append(
                    presentable_satisfaction(
                        course=course,
                        stat=section[action],
                        language=self.language
                    )
                )

        return self.data
