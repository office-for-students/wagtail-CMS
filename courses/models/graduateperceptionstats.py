from .utils import enums, separate_unavail_reason, fallback_to, display_unavailable_info


class GraduatePerceptionStatistics:

    def __init__(self, go_voice_work_data, display_language):
        self.display_language = display_language

        if go_voice_work_data:
            subject_data = fallback_to(go_voice_work_data.get('subject'), {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label', '')
            self.subject_welsh = subject_data.get('welsh_label', '')

            self.go_work_skills = fallback_to(go_voice_work_data.get('go_work_skills'), '')
            self.go_work_mean = fallback_to(go_voice_work_data.get('go_work_mean'), '')
            self.go_work_on_track = fallback_to(go_voice_work_data.get('go_work_on_track'), '')
            self.go_work_pop = fallback_to(go_voice_work_data.get('go_work_pop'), '')
            self.go_work_resp_rate = fallback_to(go_voice_work_data.get('go_work_resp_rate'), '')
            self.response_rate = fallback_to(go_voice_work_data.get('go_work_resp_rate'), '')
            self.go_work_agg = fallback_to(go_voice_work_data.get('go_work_agg'), '')
            self.aggregation_level = fallback_to(go_voice_work_data.get('go_work_agg'), '')

            unavailable_data = fallback_to(go_voice_work_data.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.display_unavailable_info = display_unavailable_info(
                self,
                aggregation_level=self.aggregation_level,
                replace=True
            )
            self.unavailable_reason_body = self.display_unavailable_info["reason_body"]

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
