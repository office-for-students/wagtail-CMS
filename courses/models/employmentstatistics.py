from CMS.enums import enums
from courses.models.utils import display_unavailable_info, new_subject_unavail


class EmploymentStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.display_stats = False
        self.aggregation_level = 0
        self.unemp_not_work_since_grad = 0
        self.doing_further_study = 0
        self.in_work = 0
        self.in_work_and_study = 0
        self.unemp_prev_emp_since_grad = 0
        self.other = 0
        self.number_of_students = 0
        self.response_rate = 0

        if data_obj:
            self.display_stats = all(
                key in data_obj for key in ['unemp_not_work_since_grad', 'doing_further_study', 'in_work',
                                            'in_work_and_study', 'unemp_prev_emp_since_grad',
                                            'other',
                                            'number_of_students', 'response_rate'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.unemp_not_work_since_grad = data_obj.get('unemp_not_work_since_grad')
            self.doing_further_study = data_obj.get('doing_further_study')
            self.in_work = data_obj.get('in_work')
            self.in_work_and_study = data_obj.get('in_work_and_study')
            self.in_work_or_study = data_obj.get('in_work_or_study')
            self.unemp_prev_emp_since_grad = data_obj.get('unemp_prev_emp_since_grad')
            self.other = data_obj.get('other')
            self.number_of_students = data_obj.get('number_of_students')
            self.response_rate = data_obj.get('response_rate')

            subject_data = data_obj.get('subject', {})
            self.subject_code = subject_data.get('code', '')
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
            if self.unavailable_code == 1 and self.aggregation_level in [None, 11, 12, 13, 21, 22, 23]:
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
            if str(self.aggregation_level) in [None, "11", "12", "13", "21", "22", "23"]:
                self.unavailable_reason_body = f"{self.unavailable_reason_heading} {self.unavailable_reason_body}"

    @property
    def work_and_or_study(self):
        return self.in_work_or_study

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
