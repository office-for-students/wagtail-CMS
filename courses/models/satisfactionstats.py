from core.utils import enums
from .satisfactionquestion import SatisfactionQuestion
from .utils import display_unavailable_info, new_subject_unavail
from .utils import separate_unavail_reason
from ..unavail_dict_cy import unavail_cy
from ..unavail_english_dict import unavail_en


class SatisfactionStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.aggregation_level = data_obj.get('aggregation_level')
        self.aggregation_year = data_obj.get('aggregation_year')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = data_obj.get('response_rate')
        self.nss_country_population = data_obj.get('nss_country_population')
        self.nss_country_aggregation = data_obj.get('nss_country_aggregation')
        self.nss_country_year = data_obj.get('nss_country_aggregation_year')
        self.nss_country_response_rate = data_obj.get('nss_country_response_rate')
        self.nss_country_subject = data_obj.get('nss_country_subject')
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
        self.question_28 = SatisfactionQuestion(data_obj.get('question_28'))

        self.nss_country_unavailable = data_obj.get('nss_country_unavailable_code')

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

        #TEMP FIX AS UNAVAIL WAS NOT INGESTED FOR NSS
        if self.aggregation_level and self.aggregation_level != 14:
            self.temp_unavail = self.get_unavail_from_code(data_obj, language)
            self.sep_unavail = separate_unavail_reason(self.temp_unavail)
            self.unavail = {"reason_heading": self.sep_unavail[0], "reason_body": self.sep_unavail[1]}

        self.unavailable_reason_heading = self.display_unavailable_info["reason_heading"]
        self.unavailable_reason_body = self.display_unavailable_info["reason_body"]
        if str(self.aggregation_level) in [None, "11", "12", "13", "21", "22", "23"]:
            self.unavailable_reason_body = f"{self.unavailable_reason_heading} {self.unavailable_reason_body}"


    def show_teaching_stats(self):
        return self.question_1.show_data_point or self.question_2.show_data_point or \
               self.question_3.show_data_point or self.question_4.show_data_point

    def show_learning_opps_stats(self):
        return self.question_5.show_data_point or self.question_6.show_data_point or \
               self.question_7.show_data_point or self.question_8.show_data_point or \
               self.question_9.show_data_point

    def show_assessment_stats(self):
        return self.question_10.show_data_point or self.question_11.show_data_point or \
               self.question_12.show_data_point or self.question_13.show_data_point or \
               self.question_14.show_data_point

    def show_support_stats(self):
        return self.question_15.show_data_point or self.question_16.show_data_point

    def show_organisation_stats(self):
        return self.question_17.show_data_point or self.question_18.show_data_point

    def show_learning_resources_stats(self):
        return self.question_19.show_data_point or self.question_20.show_data_point or \
               self.question_21.show_data_point

    def show_voice_stats(self):
        return self.question_22.show_data_point or self.question_23.show_data_point or \
               self.question_24.show_data_point or self.question_25.show_data_point

    def show_satisfaction_stats(self):
        return self.show_teaching_stats() or self.show_learning_opps_stats() or self.show_assessment_stats() or \
               self.show_organisation_stats() or self.show_learning_resources_stats() or self.show_voice_stats()

    def show_nhs_stats(self):
        return self.question_1.show_data_point or self.question_2.show_data_point or \
               self.question_3.show_data_point or self.question_4.show_data_point or \
               self.question_5.show_data_point or self.question_6.show_data_point

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english

    def teaching_stats(self):
        return [self.question_1, self.question_2,
               self.question_3, self.question_4]

    def learning_opps_stats(self):
        return [self.question_5, self.question_6,
                self.question_7, self.question_8, self.question_9]

    def assessment_stats(self):
        return [self.question_10, self.question_11, self.question_12,
               self.question_13, self.question_14]

    def support_stats(self):
        return [self.question_15, self.question_16]

    def organisation_stats(self):
        return [self.question_17, self.question_18]

    def learning_resources_stats(self):
        return [self.question_19, self.question_20, self.question_21]

    def voice_stats(self):
        return [self.question_22, self.question_23,
               self.question_24, self.question_25]

    def wellbeing_stats(self):
        return [self.question_26]

    def freedom_stats(self):
        return [self.question_27]

    def all_accordions(self):
        return [
            self.teaching_stats(), self.learning_opps_stats(), self.assessment_stats(),
            self.support_stats(), self.organisation_stats(), self.organisation_stats(),
            self.learning_resources_stats(), self.voice_stats(), self.wellbeing_stats(),
            self.freedom_stats()
        ]

    def get_unavail_from_code(self, data, language):
        unavail_code = data.get("unavailable_code", data.get("nss_country_unavailable_code"))
        aggregation_level = data.get("aggregation_level", data.get("nss_country_aggregation_level"))
        resp_rate = self.check_response_rate_present(data.get("response_rate", None))
        subject = self.display_subject_name()
        has_data = self.show_satisfaction_stats()
        return self.get_reason_from_dict(unavail_code, aggregation_level, resp_rate, subject, has_data, language)

    @staticmethod
    def check_response_rate_present(resp_rate) -> str:
        if resp_rate is None:
            return "no_resp_rate"
        return "yes_resp_rate"

    @staticmethod
    def get_reason_from_dict(unavail_code: int, aggregation_level: int, resp: str, subject: str, has_data: bool,
                             language: str) -> str:
        unavail_dict = unavail_en if language == "en" else unavail_cy
        if not has_data:
            return unavail_dict["no-data"][str(unavail_code)]
        unavail = unavail_dict["data"][str(unavail_code)][str(aggregation_level)][resp]
        unavail.replace("[Subject]", subject)
        return unavail
