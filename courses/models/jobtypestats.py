from .utils import enums, separate_unavail_reason, fallback_to


class JobTypeStatistics:

    def __init__(self, data_obj, language):
        self.display_stats = False
        self.display_language = language
        self.aggregation_level = 0
        self.non_professional_or_managerial_jobs = 0
        self.professional_or_managerial_jobs = 0
        self.unknown_professions = 0
        self.number_of_students = 0
        self.response_rate = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['non_professional_or_managerial_jobs',
                                                                 'professional_or_managerial_jobs', 'response_rate',
                                                                 'unknown_professions', 'number_of_students'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.non_professional_or_managerial_jobs = fallback_to(data_obj.get('non_professional_or_managerial_jobs'),
                                                                   0)
            self.professional_or_managerial_jobs = fallback_to(data_obj.get('professional_or_managerial_jobs'), 0)
            self.unknown_professions = fallback_to(data_obj.get('unknown_professions'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)
            self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'

            subject_data = fallback_to(data_obj.get('subject'), {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label', '')
            self.subject_welsh = subject_data.get('welsh_label', '')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')
            self.unavailable_reason_heading = self.display_unavailable_info()["reason_heading"]
            self.unavailable_reason_body = self.display_unavailable_info()["reason_body"]

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

        if self.display_language == enums.languages.ENGLISH:
            unavailable["url"] = self.unavailable_url_english if self.unavailable_url_english \
                else self.unavailable_url_welsh
        else:
            unavailable[
                "url"] = self.unavailable_url_welsh if self.unavailable_url_welsh else self.unavailable_url_english

        if "reason" in unavailable:
            if self.aggregation_level in [21, 22, 23]:
                if self.display_language == enums.languages.ENGLISH:
                    unavailable["reason"] = unavailable["reason"].replace(" over the previous two years", "")
                else:
                    unavailable["reason"] = unavailable["reason"].replace("eraill yn ystod y ddwy flynedd flaenorol",
                                                                          "eraill")

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable
