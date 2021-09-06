from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from CMS import translations
from courses.models import Course

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
    def multiple_subjects(cls, course: Course, stat: str, model_list: str, language: str, suffix=""):
        response = dict(subject=[], values=[])

        for index, subject in enumerate(course.subject_names):
            subject_name = subject.display_subject_name()
            values = "no_data"

            if index < len(getattr(course, model_list)):
                _object = getattr(course, model_list)[index]
                method = str(getattr(_object, stat))
                values = f"{method}{suffix}" if method else values

            response["subject"].append(subject_name)
            response["values"].append(values)
        return response

    @classmethod
    def presentable_data(cls, course: Course, stat: str, model_list: str, language: str, multiple=False, suffix="") -> str:
        response = "no_data"
        try:
            if multiple and course.has_multiple_subject_names:
                response = cls.multiple_subjects(
                    course=course,
                    stat=stat,
                    model_list=model_list,
                    language=language,
                    suffix=suffix
                )
            else:
                _object = getattr(course, model_list)[0]
                method = str(getattr(_object, stat))
                if method:
                    response = f"{method}{suffix}"
        except Exception as e:
            print("error: ", model_list, e)
            pass

        return response


