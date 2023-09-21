from CMS.enums import enums
from courses.models.utils import display_unavailable_info, new_subject_unavail


class GraduatePerceptionStatistics:

    def __init__(self, go_voice_work_data, display_language):
        self.display_language = display_language

        if go_voice_work_data:
            subject_data = go_voice_work_data.get('subject', {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label')
            self.subject_welsh = subject_data.get('welsh_label')

            self.go_work_skills = go_voice_work_data.get('go_work_skills')
            self.go_work_mean = go_voice_work_data.get('go_work_mean')
            self.go_work_on_track = go_voice_work_data.get('go_work_on_track')
            self.go_work_pop = go_voice_work_data.get('go_work_pop')
            self.go_work_resp_rate = go_voice_work_data.get('go_work_resp_rate')
            self.response_rate = go_voice_work_data.get('go_work_resp_rate')
            self.go_work_agg = go_voice_work_data.get('go_work_agg')
            self.aggregation_level = go_voice_work_data.get('go_work_agg')
            self.aggregation_year = go_voice_work_data.get('aggregation_year')

            unavailable_data = go_voice_work_data.get('unavailable', {})
            if unavailable_data == "":
                unavailable_data = {}

            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason', '')
            self.unavailable_reason_english = unavailable_data.get('reason_english', '')
            self.unavailable_reason_welsh = unavailable_data.get('reason_welsh', '')
            self.unavailable_find_out_more_english = unavailable_data.get('find_out_more_english', '')
            self.unavailable_find_out_more_welsh = unavailable_data.get('find_out_more_welsh', '')
            #For some reason this is the only aggregation level that comes through as a string rather than an int
            if self.aggregation_level:
                self.aggregation_level = int(self.aggregation_level)
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
            if str(self.aggregation_level) in ["11", "12", "13", "21", "22", "23"]:
                self.unavailable_reason_body = f"{self.unavailable_reason_heading} {self.unavailable_reason_body}"

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
