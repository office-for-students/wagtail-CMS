import logging
from typing import Any
from typing import List
from typing import Tuple

from CMS.translations import translations
from courses.models import Course
from courses.renderer.sections.base import Section
from courses.renderer.sections.unavailable import get_unavailable

OVERALL_SATISFACTION = "overall_satisfied"
PERCENTAGE_THOSE_ASKED = "percent_of_those_asked"

satisfaction_list = [
    "question_28",
    "nss_country_population",
    "nss_country_response_rate",
]

primary_key = 0
action = 1
suffix_index = 2
model_array = 3


logger = logging.getLogger(__name__)

class SatisfactionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, Any, Any]]:
        self.sections = [
            (OVERALL_SATISFACTION, satisfaction_list[0], "%", "satisfaction_stats", "question_28"),
            (self.DATA_FROM_PEOPLE, satisfaction_list[1], "", "satisfaction_stats", "question_28"),
            (PERCENTAGE_THOSE_ASKED, satisfaction_list[2], "%", "satisfaction_stats", "question_28"),
            (self.DATA_DISPLAYED, "", "", "satisfaction_stats", True, "question_28")
        ]

        return self.sections

    @classmethod
    def presentable_data(
            cls,
            course: Course,
            stat: str,
            model_list: str,
            language: str,
            multiple=False,
            suffix="",
            unavailable=False,
            custom_unavail=None

    ):
        if cls.check_if_custom_unavail(course, custom_unavail):
            response = cls.set_custom_unavail(custom_unavail, language)
        else:
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
                if not unavailable and not custom_unavail:
                    method = getattr(_object, stat)
                    if method is not None:
                        response = f"{method}{suffix}"
        except Exception as e:
            logger.warning(e.__cause__)
            pass

        return response

    @classmethod
    def check_unavailable_england(cls, course: Course, custom_unavail):
        return course.country.code == "XF" and custom_unavail == "question_28"

    @classmethod
    def check_unavailable_ni_scot_wales(cls, course: Course, custom_unavail):
        return course.country.code != "XF" and custom_unavail == "question_27"

    @classmethod
    def check_if_custom_unavail(cls, course: Course, custom_unavail: str) -> bool:
        return cls.check_unavailable_england(course, custom_unavail) or cls.check_unavailable_ni_scot_wales(course, custom_unavail)

    @staticmethod
    def set_custom_unavail(custom_unavail: str, language: str, index=0):
        header = translations.term_for_key(key="no_data_available", language=language)
        body = translations.term_for_key(key=f"{custom_unavail}_unavailable", language=language)
        return ["unavailable", header, body, index]

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.sections:
                custom_unavail = None
                if section[-1] in ["question_27", "question_28"]:
                    custom_unavail = section[-1]
                self.data[section[primary_key]]["values"].append(
                    self.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list=section[model_array],
                        language=self.language,
                        suffix=section[suffix_index],
                        multiple=True,
                        unavailable=self.check_unavailable(section),
                        custom_unavail=custom_unavail
                    )
                )
        return self.data


class SubSatisfactionSection(Section):

    def get_sections(self) -> List[Tuple[Any, Any, str, str]]:
        sections = []

        for index, i in enumerate(self.keys):
            if index == 0:
                if not i == 27:
                    sections.append((self.DATA_DISPLAYED, "", "", "satisfaction_stats", True))
                else:
                    sections.append((self.DATA_DISPLAYED, "", "", "satisfaction_stats", True, "question_27"))
            if not i == 27:
                sections.append((f"question_{i}", f"question_{i}", "%", "satisfaction_stats"))
            else:

                sections.append((f"question_{i}", f"question_{i}", "%", "satisfaction_stats", "question_27"))
        return sections

    def generate_dict(self) -> dict:
        for course in self.courses:
            for section in self.sections:
                custom_unavail = None
                if section[-1] == "question_27":
                    custom_unavail = section[-1]
                self.data[section[primary_key]]["values"].append(
                    self.presentable_data(
                        course=course,
                        stat=section[action],
                        model_list=section[model_array],
                        language=self.language,
                        suffix=section[suffix_index],
                        multiple=True,
                        unavailable=self.check_unavailable(section),
                        custom_unavail=custom_unavail
                    )
                )

        return self.data

    @classmethod
    def presentable_data(
            cls,
            course: Course,
            stat: str,
            model_list: str,
            language: str,
            multiple=False,
            suffix="",
            unavailable=False,
            custom_unavail=None

    ):
        country_unavail = False
        if cls.check_unavailable_ni_scot_wales(course, custom_unavail):
            country_unavail = True
            response = cls.set_custom_unavail(custom_unavail, language)
        else:
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
                    unavailable=unavailable,
                )
            else:
                if not unavailable and not country_unavail:
                    method = getattr(_object, stat)
                    if method is not None:
                        response = f"{method}{suffix}"
        except Exception as e:
            logger.warning(e.__cause__)
            pass

        return response

    @classmethod
    def check_unavailable_england(cls, course: Course, custom_unavail):
        return course.country.code == "XF" and custom_unavail == "question_28"

    @classmethod
    def check_unavailable_ni_scot_wales(cls, course: Course, custom_unavail):
        return course.country.code != "XF" and custom_unavail == "question_27"

    @classmethod
    def check_if_custom_unavail(cls, course: Course, custom_unavail: str) -> bool:
        return cls.check_unavailable_england(course, custom_unavail) or cls.check_unavailable_ni_scot_wales(course,
                                                                                                            custom_unavail)

    @staticmethod
    def set_custom_unavail(custom_unavail: str, language: str, index=0):
        header = translations.term_for_key(key="no_data_available", language=language)
        body = translations.term_for_key(key=f"{custom_unavail}_unavailable", language=language)
        return ["unavailable", header, body, index]

