from CMS.enums import enums
from courses.models.utils import display_unavailable_info, new_subject_unavail


class EntryStatistics:

    def __init__(self, data_obj, display_language):
        self.display_language = display_language
        self.display_stats = False
        self.aggregation_level = 0
        self.number_of_students = 0
        self.a_level = 0
        self.access = 0
        self.another_higher_education_qualifications = 0
        self.baccalaureate = 0
        self.degree = 0
        self.foundation = 0
        self.none = 0
        self.other_qualifications = 0
        self.unavailable_code = ''
        self.unavailable_reason = ''

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['a-level', 'access',
                                                                 'another_higher_education_qualifications',
                                                                 'baccalaureate', 'degree', 'foundation', 'none',
                                                                 'other_qualifications', 'number_of_students'])

            self.aggregation_level = data_obj.get('aggregation_level', 0)
            self.number_of_students = data_obj.get('number_of_students')

            self.a_level = data_obj.get('a-level')
            self.access = data_obj.get('access')
            self.another_higher_education_qualifications = data_obj.get('another_higher_education_qualifications')
            self.baccalaureate = data_obj.get('baccalaureate')
            self.degree = data_obj.get('degree')
            self.foundation = data_obj.get('foundation')
            self.none = data_obj.get('none')
            self.other_qualifications = data_obj.get('other_qualifications')
            subject_data = data_obj.get('subject', {})

            self.subject_code = subject_data.get('code')
            self.subject_english = subject_data.get('english_label')
            self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = data_obj.get('unavailable', {})
            if unavailable_data == "":
                unavailable_data = {}
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason', '')
            self.unavailable_reason_english = unavailable_data.get('reason_english', '')
            self.unavailable_reason_welsh = unavailable_data.get('reason_welsh', '')
            self.unavailable_find_out_more_english = unavailable_data.get('find_out_more_english', '')
            self.unavailable_find_out_more_welsh = unavailable_data.get('find_out_more_welsh', '')
            self.unavailable_url_english = unavailable_data.get('url_english', '')
            self.unavailable_url_welsh = unavailable_data.get('url_welsh', '')
            if self.unavailable_code == 1 and self.aggregation_level in ["", 11, 12, 13, 21, 22, 23]:
                self.display_unavailable_info = new_subject_unavail(
                    aggregation_level=self.aggregation_level,
                    subject_title_in_local_language=self.display_subject_name(),
                    language=self.display_language
                )
            else:
                self.display_unavailable_info = display_unavailable_info(
                    self,
                    aggregation_level=self.aggregation_level,
                    subject_welsh=self.subject_welsh
                )
            self.unavailable_reason_heading = self.display_unavailable_info["reason_heading"]
            self.unavailable_reason_body = self.display_unavailable_info["reason_body"]
            if str(self.aggregation_level) in ["11", "12", "13", "21", "22", "23"]:
                self.unavailable_reason_body = f"{self.unavailable_reason_heading} {self.unavailable_reason_body}"

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
   