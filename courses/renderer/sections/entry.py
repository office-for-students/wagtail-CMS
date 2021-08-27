from typing import List, Tuple, Any, Dict
from courses.renderer.sections.base import Section

DATA_FROM_PEOPLE = "data_from_people"
A_LEVEL = "a_level_similar"
BACCALAUREATE = "baccalaureate"
DEGREE = "degree"
OTHER_HIGHER_QUALIFICATION = "other_higher_qualifications"
ACCESS_COURSE = "access_course"
FOUNDATION_COURSE = "foundation_course"
NO_QUALIFICATIONS = "no_qualifications"
OTHER = "other"
TYPICAL_RANGE = "typical_range"

entry_list = [
    "number_of_students",
    "a_level",
    "baccalaureate",
    "degree",
    "another_higher_education_qualifications",
    "access",
    "foundation",
    "none",
    "other"
]
tariff_list = [
    "number_of_students",
    "range",
]

primary_key = 1
action = 2
suffix_index = 3
model_index = 4


class SubEntrySection(Section):

    def __init__(self, keys: List, courses, language='en'):
        self.start_range = keys[0]
        self.end_range = keys[1]
        super().__init__(courses, language)

    def get_sections(self) -> List[Tuple[Any, Any, Any, str]]:
        sub_sections = []
        sections = [
            (
                ("1", DATA_FROM_PEOPLE, entry_list[0], "", "entry_stats"),
                ("2", A_LEVEL, entry_list[1], "%", "entry_stats"),
                ("3", BACCALAUREATE, entry_list[2], "%", "entry_stats"),
                ("4", DEGREE, entry_list[3], "%", "entry_stats"),
                ("5", OTHER_HIGHER_QUALIFICATION, entry_list[4], "%", "entry_stats"),
                ("6", ACCESS_COURSE, entry_list[5], "%", "entry_stats"),
                ("7", FOUNDATION_COURSE, entry_list[6], "%", "entry_stats"),
                ("8", NO_QUALIFICATIONS, entry_list[7], "%", "entry_stats"),
                ("9", OTHER, entry_list[8], "%", "entry_stats"),

                ("10", DATA_FROM_PEOPLE, tariff_list[0], "", "tariff_stats"),
                ("11", TYPICAL_RANGE, tariff_list[1], "", "tariff_stats"),

            )]

        for i in range(self.start_range, self.end_range):
            sub_sections.append((sections[0][i]))
        return sub_sections

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
                        model_list=section[model_index],
                        language=self.language,
                        multiple=False,
                        suffix=section[suffix_index]
                    )
                )
        return self.data


