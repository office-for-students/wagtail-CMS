from CMS.enums import enums
from .tariff import Tariff
from .tariff import tariff_range
from .utils import display_unavailable_info, new_subject_unavail


class TariffStatistics:

    def __init__(self, tariff_data, display_language):
        self.display_language = display_language
        self.tariffs = []
        self.tariff_list = []

        if tariff_data:
            self.aggregation_level = tariff_data.get('aggregation_level')
            self.aggregation_year = tariff_data.get('aggregation_year')
            self.number_of_students = tariff_data.get('number_of_students')
            if tariff_data.get('tariffs'):
                for tariff in tariff_data.get('tariffs'):
                    self.tariffs.append(Tariff(tariff, self.display_language))
                    if tariff["entrants"] != 0:
                        self.tariff_list.append(tariff)
            self.tariffs.reverse()
            if self.tariff_list:
                self.range = tariff_range(self.tariff_list, self.display_language)

            subject_data = tariff_data.get('subject', {})
            self.subject_code = subject_data.get('code')
            self.subject_english = subject_data.get('english_label')
            self.subject_welsh = subject_data.get('welsh_label')

            unavailable_data = tariff_data.get('unavailable', {})
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
            if str(self.aggregation_level) in ["11", "12", "13", "21", "22", "23"]:
                self.unavailable_reason_body = f"{self.unavailable_reason_heading} {self.unavailable_reason_body}"

    def show_stats(self):
        return self.tariffs

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
