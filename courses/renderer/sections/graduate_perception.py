from typing import List, Tuple, Any, Dict

from CMS import translations
from courses.models import Course
from courses.renderer.sections.base import Section
from courses.renderer.sections.unavailable import get_unavailable

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


    #TODO: Remove below method and use set_unavailable from base class when OFS want to remove the unavailable message override.
    # https://app.clickup.com/t/j337mq
    @classmethod
    def set_unavailable(
            cls,
            course: Course,
            model_list: str,
            language: str,
            index=0
    ):
        try:
            accordion = translations.term_for_key(key="graduate_perceptions", language=language)
            _object = getattr(course, model_list)[index]
            body = getattr(_object, "unavailable_reason_body")
            header = get_unavailable(course, model_list, language, accordion)["header"]
        except Exception as e:
            header = translations.term_for_key(key="no_data_available", language=language)
            _object = getattr(course, "display_no_data")()
            body = _object["reason"]

        return ["unavailable", header, body]
    # end remove
