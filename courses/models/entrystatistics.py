from .utils import enums, separate_unavail_reason, fallback_to


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

            self.aggregation_level = fallback_to(data_obj.get('aggregation_level'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)

            self.a_level = fallback_to(data_obj.get('a-level'), 0)
            self.access = fallback_to(data_obj.get('access'), 0)
            self.another_higher_education_qualifications = fallback_to(
                data_obj.get('another_higher_education_qualifications'), 0)
            self.baccalaureate = fallback_to(data_obj.get('baccalaureate'), 0)
            self.degree = fallback_to(data_obj.get('degree'), 0)
            self.foundation = fallback_to(data_obj.get('foundation'), 0)
            self.none = fallback_to(data_obj.get('none'), 0)
            self.other_qualifications = fallback_to(data_obj.get('other_qualifications'), 0)

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

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    # TODO refactor all these same functions to a shared one
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

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable
