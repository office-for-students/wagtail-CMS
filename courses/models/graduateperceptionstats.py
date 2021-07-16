from .utils import enums, separate_unavail_reason, fallback_to


class GraduatePerceptionStatistics:

    def __init__(self, go_voice_work_data, display_language):
        self.display_language = display_language

        if go_voice_work_data:
            subject_data = fallback_to(go_voice_work_data.get('subject'), {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label', '')
            self.subject_welsh = subject_data.get('welsh_label', '')

            unavailable_data = fallback_to(go_voice_work_data.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')

            self.go_work_skills = fallback_to(go_voice_work_data.get('go_work_skills'), '')
            self.go_work_mean = fallback_to(go_voice_work_data.get('go_work_mean'), '')
            self.go_work_on_track = fallback_to(go_voice_work_data.get('go_work_on_track'), '')
            self.go_work_pop = fallback_to(go_voice_work_data.get('go_work_pop'), '')
            self.go_work_resp_rate = fallback_to(go_voice_work_data.get('go_work_resp_rate'), '')
            self.go_work_agg = fallback_to(go_voice_work_data.get('go_work_agg'), '')

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def display_unavailable_info(self):
        unavailable = {}

        if self.unavailable_reason:
            unavailable["reason"] = self.unavailable_reason
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable["reason"] = self.unavailable_reason_english if self.unavailable_reason_english \
                    else self.unavailable_reason_welsh
            else:
                unavailable[
                    "reason"] = self.unavailable_reason_welsh if self.unavailable_reason_welsh else self.unavailable_reason_english

        if self.display_language == enums.languages.ENGLISH:
            unavailable[
                "find_out_more"] = self.unavailable_find_out_more_english if self.unavailable_find_out_more_english \
                else self.unavailable_find_out_more_welsh
        else:
            unavailable[
                "find_out_more"] = self.unavailable_find_out_more_welsh if self.unavailable_find_out_more_welsh else self.unavailable_find_out_more_english

        if "reason" in unavailable:
            if self.go_work_agg in ["21", "22", "23"]:
                if self.display_language == enums.languages.ENGLISH:
                    unavailable["reason"] = unavailable["reason"].replace(" over the previous two years", "")
                else:
                    unavailable["reason"] = unavailable["reason"].replace("eraill yn ystod y ddwy flynedd flaenorol",
                                                                          "eraill")

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable
