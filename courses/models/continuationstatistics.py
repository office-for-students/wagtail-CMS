from .utils import fallback_to, enums, separate_unavail_reason, display_unavailable_info


class ContinuationStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.display_stats = False
        self.dormant = 0
        self.continuing = 0
        self.gained = 0
        self.left = 0
        self.lower = 0
        self.number_of_students = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['dormant', 'continuing_with_provider', 'gained',
                                                                 'left', 'lower'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)

            self.dormant = fallback_to(data_obj.get('dormant'), 0)
            self.continuing = fallback_to(data_obj.get('continuing_with_provider'), 0)
            self.gained = fallback_to(data_obj.get('gained'), 0)
            self.left = fallback_to(data_obj.get('left'), 0)
            self.lower = fallback_to(data_obj.get('lower'), 0)

            subject_data = data_obj.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = fallback_to(data_obj.get('unavailable'), {})
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')
            self.unavailable_reason_english = fallback_to(unavailable_data.get('reason_english'), '')
            self.unavailable_reason_welsh = fallback_to(unavailable_data.get('reason_welsh'), '')
            self.unavailable_find_out_more_english = fallback_to(unavailable_data.get('find_out_more_english'), '')
            self.unavailable_find_out_more_welsh = fallback_to(unavailable_data.get('find_out_more_welsh'), '')
            self.unavailable_url_english = fallback_to(unavailable_data.get('url_english'), '')
            self.unavailable_url_welsh = fallback_to(unavailable_data.get('url_welsh'), '')
            self.display_unavailable_info = display_unavailable_info(
                self,
                aggregation_level=self.aggregation_level,
            )
            self.unavailable_reason_heading = self.display_unavailable_info["reason_heading"]
            self.unavailable_reason_body = self.display_unavailable_info["reason_body"]
            if str(self.aggregation_level) in ["11", "12", "13", "21", "22", "23"]:
                self.unavailable_reason_body = f"{self.unavailable_reason_heading} {self.unavailable_reason_body}"

    @property
    def continuing_or_complete(self):
        return self.continuing + self.gained

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
