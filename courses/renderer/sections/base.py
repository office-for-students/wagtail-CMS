import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from CMS import translations
from courses.models import Course
from courses.renderer.sections.unavailable import get_unavailable

primary_key = 0
action = 1

logger = logging.getLogger(__name__)


class Section:
    DATA_DISPLAYED = "data_displayed"
    DATA_FROM_PEOPLE = "data_from_people"

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
        response = dict(values=[])

        for index, subject in enumerate(course.subject_names):

            if unavailable:
                response["values"].append(
                    cls.set_unavailable(course=course, model_list=model_list, index=index, language=language))
                continue

            if index < len(getattr(course, model_list)):
                _object = getattr(course, model_list)[index]
                method = getattr(_object, stat)
                if method is not None:
                    response["values"].append(f"{method}{suffix}")
                else:
                    response["values"].append(
                        cls.set_unavailable(course=course, model_list=model_list, index=index, language=language))
            else:
                response["values"].append(
                    cls.set_unavailable(course=course, model_list=model_list, index=index, language=language))

        return response

    @classmethod
    def presentable_data(
            cls,
            course: Course,
            stat: str,
            model_list: str,
            language: str,
            multiple=False,
            suffix="",
            unavailable=False
    ):
        response = cls.set_unavailable(course=course, model_list=model_list, language=language)
        _object = getattr(course, model_list)[0]
        try:
            if multiple and course.has_multiple_subject_names:
                return cls.multiple_subjects(
                    course=course,
                    stat=stat,
                    model_list=model_list,
                    language=language,
                    suffix=suffix,
                    unavailable=unavailable
                )
            else:
                if not unavailable:
                    method = getattr(_object, stat)
                    if method is not None:
                        response = f"{method}{suffix}"
        except Exception as e:
            logger.warning(e.__cause__)
            pass

        return response

    @classmethod
    def set_unavailable(cls, course: Course, model_list: str, language: str, index=0):
        # noinspection PyBroadException
        if index < len(getattr(course, model_list)):
            _object = getattr(course, model_list)[index]
            body = getattr(_object, "unavailable_reason_body")
            header = get_unavailable(course, model_list, language)
        else:
            header = translations.term_for_key(key="no_data_available", language=language)
            _object = getattr(course, "display_no_data")()
            body = _object["reason"]

        return ["unavailable", header, body, index]

    @staticmethod
    def check_unavailable(section):
        unavailable = True if section[-1] is True else False
        return unavailable
