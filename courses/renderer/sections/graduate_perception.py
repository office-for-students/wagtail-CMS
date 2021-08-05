from typing import List, Tuple, Any, Dict

from courses.models import Course
from courses.renderer.sections.base import Section

DATA_FROM_PEOPLE = "data_from_people"
USEFULNESS = "usefulness"
MEANINGFULNESS = "meaningfulness"
FUTURE = "future"

graduate_list = [
    "go_work_pop",
    "go_work_skills",
    "go_work_mean",
    "go_work_on_track"
]

primary_key = 1
action = 2
suffix_index = 3


def presentable_graduate(course: Course, stat: str, suffix: Any, language: str) -> str:
    if language == 'cy':
        response = "Nid yw'r data ar gael"
    else:
        response = "No data available"
    try:
        _object = course.graduate_perceptions[0]
        method = str(getattr(_object, stat))
        response = f"{method}{suffix}" if suffix and method.isnumeric() else method
    except Exception as e:
        print("error: ", e)
        pass
    return response


class GraduatePerceptionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, Any, str]]:
        sections = [
                ("1", DATA_FROM_PEOPLE, graduate_list[0], None),
                ("2", USEFULNESS, graduate_list[1], "%"),
                ("3", MEANINGFULNESS, graduate_list[2], "%"),
                ("4", FUTURE, graduate_list[3], "%"),
            ]
        return sections

    def prep_data(self):
        self.data = {}
        self.sections = self.get_sections()
        for section in self.sections:
            self.data[section[0]] = self.empty_data_structure(section[primary_key], self.language)

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.sections:
                self.data[section[0]]["values"].append(
                    presentable_graduate(
                        course=course,
                        stat=section[action],
                        suffix=section[suffix_index],
                        language=self.language
                    )
                )
        self.update_data_with_subtitles(self.data)
        return self.data

    def update_data_with_subtitles(self, data: Dict[str, Any]):
        subtitles = {
            "2": "usefulness_subtitle",
            "3": "meaningfulness_subtitle",
            "4": "future_subtitle"
        }
        for section in self.sections:
            if section[0] in subtitles:
                data[section[0]]["subtitle"] = self.term_for_key(subtitles[section[0]], self.language)
