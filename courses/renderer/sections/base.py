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
    def multiple_subjects(cls, course: Course, stat: str, model_list: str, language: str, suffix=""):
        response = dict(subject=[], values=[])
        values = cls.unavailable_message(
            course=course,
            model_list=model_list,
            language=language,
            present_as_multiple=True
        )

        for index, subject in enumerate(course.subject_names):
            subject_name = subject.display_subject_name()

            if index < len(getattr(course, model_list)):
                _object = getattr(course, model_list)[index]
                method = str(getattr(_object, stat))
                if method:
                    values = f"{method}{suffix}"

            response["subject"].append(subject_name)
            response["values"].append(values)
        return response

    @classmethod
    def presentable_data(cls, course: Course, stat: str, model_list: str, language: str, multiple=False, suffix="") -> str:
        response = cls.unavailable_message(
            course=course,
            model_list=model_list,
            language=language,
            present_as_multiple=False
        )
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

    @classmethod
    def unavailable_message(cls, course, model_list, language, present_as_multiple):
        unavailable = get_unavailable(
            course=course,
            model_list=model_list,
            language=language,
            present_as_multiple=present_as_multiple
        )
        header = unavailable["header"]
        message = unavailable["message"]
        response = [header, message, "unavailable"]

        return response
