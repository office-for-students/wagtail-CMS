from typing import List, Tuple, Any, Dict

from CMS import translations
from courses.models import Course
from courses.renderer.sections.base import Section

PERCENTAGE_THOSE_ASKED = "percent_of_those_asked"
USEFULNESS = "usefulness"
MEANINGFULNESS = "meaningfulness"
FUTURE = "future"

graduate_list = [
    "go_work_pop",
    "response_rate",
    "go_work_skills",
    "go_work_mean",
    "go_work_on_track"
]

primary_key = 1
action = 2
suffix_index = 3
model_array = 4


def multiple_subjects(course: Course, stat: str, suffix: Any, language: str) -> dict:
    response = dict(subject=[], values=[])
    for index, subject in enumerate(course.subject_names):
        subject_name = subject.display_subject_name()
        if index < len(course.graduate_perceptions):
            _object = course.graduate_perceptions[index]
            method = str(getattr(_object, stat))
            response["values"].append(f"{method}{suffix}" if suffix and method.isnumeric() else method)
            response["subject"].append(subject_name)
        else:
            response["values"].append(translations.term_for_key(key="no_data_available", language=language))
    return response


def presentable_graduate(course: Course, stat: str, suffix: Any, language: str) -> str:
    response = translations.term_for_key(key="no_data_available", language=language)
    try:
        if course.has_multiple_subject_names:
            response = multiple_subjects(course, stat, suffix, language)
        else:
            _object = course.graduate_perceptions[0]
            method = str(getattr(_object, stat))
            if method:
                response = f"{method}{suffix}" if suffix and method.isnumeric() else method
    except Exception as e:
        print("error: ", e)
        pass
    return response


class GraduatePerceptionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, Any, str, str]]:
        sections = [
                ("0", self.DATA_DISPLAYED, "", "", "graduate_perceptions", True),
                ("1", self.DATA_FROM_PEOPLE, graduate_list[0], "", "graduate_perceptions"),
                ("2", PERCENTAGE_THOSE_ASKED, graduate_list[1], "%", "graduate_perceptions"),
                ("3", USEFULNESS, graduate_list[2], "%", "graduate_perceptions"),
                ("4", MEANINGFULNESS, graduate_list[3], "%", "graduate_perceptions"),
                ("5", FUTURE, graduate_list[4], "%", "graduate_perceptions"),
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
                    self.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list=section[model_array],
                        language=self.language,
                        multiple=True,
                        suffix=section[suffix_index],
                        unavailable=self.check_unavailable(section)
                    )
                )
        self.update_data_with_subtitles(self.data)
        return self.data

    def update_data_with_subtitles(self, data: Dict[str, Any]):
        subtitles = {
            "3": "usefulness_subtitle",
            "4": "meaningfulness_subtitle",
            "5": "future_subtitle"
        }
        for section in self.sections:
            if section[0] in subtitles:
                data[section[0]]["subtitle"] = self.term_for_key(subtitles[section[0]], self.language)
