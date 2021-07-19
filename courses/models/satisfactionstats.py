from .utils import fallback_to, enums, separate_unavail_reason
from .satisfactionquestion import SatisfactionQuestion


class SatisfactionStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.aggregation_level = data_obj.get('aggregation_level')
        self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)
        self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'
        self.question_1 = SatisfactionQuestion(data_obj.get('question_1'))
        self.question_2 = SatisfactionQuestion(data_obj.get('question_2'))
        self.question_3 = SatisfactionQuestion(data_obj.get('question_3'))
        self.question_4 = SatisfactionQuestion(data_obj.get('question_4'))
        self.question_5 = SatisfactionQuestion(data_obj.get('question_5'))
        self.question_6 = SatisfactionQuestion(data_obj.get('question_6'))
        self.question_7 = SatisfactionQuestion(data_obj.get('question_7'))
        self.question_8 = SatisfactionQuestion(data_obj.get('question_8'))
        self.question_9 = SatisfactionQuestion(data_obj.get('question_9'))
        self.question_10 = SatisfactionQuestion(data_obj.get('question_10'))
        self.question_11 = SatisfactionQuestion(data_obj.get('question_11'))
        self.question_12 = SatisfactionQuestion(data_obj.get('question_12'))
        self.question_13 = SatisfactionQuestion(data_obj.get('question_13'))
        self.question_14 = SatisfactionQuestion(data_obj.get('question_14'))
        self.question_15 = SatisfactionQuestion(data_obj.get('question_15'))
        self.question_16 = SatisfactionQuestion(data_obj.get('question_16'))
        self.question_17 = SatisfactionQuestion(data_obj.get('question_17'))
        self.question_18 = SatisfactionQuestion(data_obj.get('question_18'))
        self.question_19 = SatisfactionQuestion(data_obj.get('question_19'))
        self.question_20 = SatisfactionQuestion(data_obj.get('question_20'))
        self.question_21 = SatisfactionQuestion(data_obj.get('question_21'))
        self.question_22 = SatisfactionQuestion(data_obj.get('question_22'))
        self.question_23 = SatisfactionQuestion(data_obj.get('question_23'))
        self.question_24 = SatisfactionQuestion(data_obj.get('question_24'))
        self.question_25 = SatisfactionQuestion(data_obj.get('question_25'))
        self.question_26 = SatisfactionQuestion(data_obj.get('question_26'))
        self.question_27 = SatisfactionQuestion(data_obj.get('question_27'))

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

    def show_teaching_stats(self):
        return self.question_1.show_data_point or self.question_2.show_data_point or \
               self.question_3.show_data_point or self.question_4.show_data_point

    def show_learning_opps_stats(self):
        return self.question_5.show_data_point or self.question_6.show_data_point or \
               self.question_7.show_data_point

    def show_assessment_stats(self):
        return self.question_8.show_data_point or self.question_9.show_data_point or \
               self.question_10.show_data_point or self.question_11.show_data_point

    def show_support_stats(self):
        return self.question_12.show_data_point or self.question_13.show_data_point or \
               self.question_14.show_data_point

    def show_organisation_stats(self):
        return self.question_15.show_data_point or self.question_16.show_data_point or \
               self.question_17.show_data_point

    def show_learning_resources_stats(self):
        return self.question_18.show_data_point or self.question_19.show_data_point or \
               self.question_20.show_data_point

    def show_learning_community_stats(self):
        return self.question_21.show_data_point or self.question_22.show_data_point

    def show_voice_stats(self):
        return self.question_23.show_data_point or self.question_24.show_data_point or \
               self.question_25.show_data_point or self.question_26.show_data_point

    def show_satisfaction_stats(self):
        return self.show_teaching_stats() or self.show_learning_opps_stats() or self.show_assessment_stats() or \
               self.show_organisation_stats() or self.show_learning_resources_stats() or \
               self.show_learning_community_stats() or self.show_voice_stats()

    def show_nhs_stats(self):
        return self.question_1.show_data_point or self.question_2.show_data_point or \
               self.question_3.show_data_point or self.question_4.show_data_point or \
               self.question_5.show_data_point or self.question_6.show_data_point

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

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable