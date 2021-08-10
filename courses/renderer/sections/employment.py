from typing import List, Tuple, Any, Dict

from CMS import translations
from courses.models import Course
from courses.renderer.sections.base import Section

DATA_FROM_PEOPLE = "data_from_people"
NOW_WORKING = "now_working"
DOING_FURTHER_STUDY = "doing_further_study"
WORKING_AND_STUDYING = "study_and_working"
UNEMPLOYED = "unemployed"
UNEMPLOYED2 = "unemployed"
OTHER = "other"
HIGHLY_SKILLED = "highly_skilled"
OTHER_WORK = "other_work"
UNKNOWN_WORK = "unknown_work"

employment_list = [
    "number_of_students",
    "in_work",
    "doing_further_study",
    "in_work_and_study",
    "unemp_prev_emp_since_grad",
    "unemp_not_work_since_grad",
    "other"
]
job_types_list = [
    "number_of_students",
    "professional_or_managerial_jobs",
    "non_professional_or_managerial_jobs",
    "unknown_professions"
]

primary_key = 1
action = 2
suffix_index = 3
model_index = 4


# def multiple_subjects(course: Course, stat: str, suffix: Any, model: str, language: str) -> dict:
#     response = dict(subject=[], values=[])
#
#     for index, subject in enumerate(course.subject_names):
#         subject_name = subject.display_subject_name()
#         values = translations.term_for_key(key="no_data_available", language=language)
#
#         if model == "employment":
#             if index < len(course.employment_stats):
#                 _object = course.employment_stats[index]
#                 method = str(getattr(_object, stat))
#                 values = f"{method}{suffix}" if suffix and method.isnumeric() else method
#         else:
#             if index < len(course.job_type_stats):
#                 _object = course.job_type_stats[index]
#                 method = str(getattr(_object, stat))
#                 values = f"{method}{suffix}" if suffix and method.isnumeric() else method
#
#         response["subject"].append(subject_name)
#         response["values"].append(values)
#     return response





class SubEmploymentSection(Section):

    def __init__(self, keys: List, courses, language='en'):
        self.start_range = keys[0]
        self.end_range = keys[1]
        super().__init__(courses, language)

    def get_sections(self) -> List[Tuple[Any, Any, Any, str]]:
        sub_sections = []
        sections = [
            (
                ("1", DATA_FROM_PEOPLE, employment_list[0], "", "employment_stats"),
                ("2", NOW_WORKING, employment_list[1], "%", "employment_stats"),
                ("3", DOING_FURTHER_STUDY, employment_list[2], "%", "employment_stats"),
                ("4", WORKING_AND_STUDYING, employment_list[3], "%", "employment_stats"),
                ("5", UNEMPLOYED, employment_list[4], "%", "employment_stats"),
                ("6", UNEMPLOYED2, employment_list[5], "%", "employment_stats"),
                ("7", OTHER, employment_list[6], "%", "employment_stats"),

                ("8", DATA_FROM_PEOPLE, job_types_list[0], "", "job_type_stats"),
                ("9", HIGHLY_SKILLED, job_types_list[1], "%", "job_type_stats"),
                ("10", OTHER_WORK, job_types_list[2], "%", "job_type_stats"),
                ("11", UNKNOWN_WORK, job_types_list[3], "%", "job_type_stats"),
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
                        suffix=section[suffix_index],
                    )
                )
        self.update_data_with_subtitles(self.data)
        return self.data

    def update_data_with_subtitles(self, data: Dict[str, Any]):
        subtitles = {
            "5": "unemp_prev_emp_since_grad",
            "6": "unemp_not_work_since_grad",
            "9": "employed_in_professional",
            "10": "employed_not_in_professional",
            "11": "employment_type_unknown"
        }
        for section in self.sections:
            if section[0] in subtitles:
                data[section[0]]["subtitle"] = self.term_for_key(subtitles[section[0]], self.language)



