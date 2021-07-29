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


def presentable_employment(course: Course, stat: str, suffix: Any, language: str) -> str:
    if language == 'cy':
        response = "Nid yw'r data ar gael"
    else:
        response = "No data available"
    try:
        _object = course.employment_stats[0]
        method = str(getattr(_object, stat))
        response = f"{method}{suffix}" if suffix and method.isnumeric() else method
    except Exception as e:
        print("error: ", e)
        pass

    return response


class SubEmploymentSection(Section):

    def __init__(self, keys: List[str], courses, language='en'):
        self.keys = keys
        super().__init__(courses, language)

    def get_sections(self) -> List[Tuple[Any, Any, Any]]:
        sections = []

        for i in self.keys:
            sections.append((f"nss_question_{i}", f"question_{i}", "%"), )
        return sections

    def generate_dict(self) -> dict:
        sections = self.get_sections()
        for course in self.courses:
            for section in sections:
                self.data[section[primary_key]]["values"].append(
                    presentable_employment(
                        course=course,
                        stat=section[action],
                        suffix=section[suffix_index],
                        language=self.language
                    )
                )

        return self.data
