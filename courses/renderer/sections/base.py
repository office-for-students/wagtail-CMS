from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable import get_unavailable

primary_key = 0
action = 1


class Section:

    def __init__(self, courses: List[Course], language: str, keys=None):
        self.keys = keys
        self.data = {}
        self.courses = courses
        self.language = language
        self.sections = None
        super().__init__()

    def term_for_key(self, key, language):
        return translations.term_for_key(key=key, language=language)

    def empty_data_structure(self, key: str, language: str) -> Dict[str, Any]:
        return dict(title=self.term_for_key(key, language), subtitle="", values=[])

    def get_sections(self) -> List[Tuple[Any, Any]]:
        raise NotImplementedError

    def prep_data(self):
        self.data = {}
        self.sections = self.get_sections()
        for section in self.sections:
            self.data[section[primary_key]] = self.empty_data_structure(section[primary_key], self.language)

    def generate_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def multiple_subjects(cls, course: Course, stat: str, model_list: str, language: str, suffix="", unavailable=False):
        response = dict(subject=[], values=[])

        for index, subject in enumerate(course.subject_names):
            subject_name = subject.display_subject_name()
            values = cls.set_unavailable(course=course, model_list=model_list, index=index, language=language)

            if (index < len(getattr(course, model_list))) and not unavailable:
                _object = getattr(course, model_list)[index]
                method = str(getattr(_object, stat))
                values = f"{method}{suffix}" if method else values

            response["subject"].append(subject_name)
            response["values"].append(values)
        return response

    @classmethod
    def presentable_data(cls, course: Course, stat: str, model_list: str, language: str, multiple=False, suffix="", unavailable=False) -> str:
        response = cls.set_unavailable(course=course, model_list=model_list, language=language)
        try:
            if multiple and course.has_multiple_subject_names:
                response = cls.multiple_subjects(
                    course=course,
                    stat=stat,
                    model_list=model_list,
                    language=language,
                    suffix=suffix,
                    unavailable=unavailable
                )
            else:
                if not unavailable:
                    _object = getattr(course, model_list)[0]
                    method = str(getattr(_object, stat))
                    if method:
                        response = f"{method}{suffix}"
        except Exception as e:
            print("error: ", model_list, e)
            pass

        return response

    @classmethod
    def set_unavailable(cls, course: Course, model_list: str, language: str, index=0):
        try:
            _object = getattr(course, model_list)[index]
            body = getattr(_object, "unavailable_reason_body")
            header = get_unavailable(course, model_list, language)["header"][0]
        except Exception as e:
            header = translations.term_for_key(key="no_data_available", language=language)
            _object = getattr(course, "display_no_data")()
            body = _object["reason"]

        return ["unavailable", header, body]

    def check_unavailable(self, section):
        unavailable = True if section[-1] is True else False
        return unavailable
