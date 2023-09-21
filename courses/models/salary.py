from CMS.translations.dictionaries.unavailable import UNAVAILABLE
from core.utils import enums
from courses.models.utils import separate_unavail_reason


class Salary:

    def __init__(self, salary_data, display_language, institution_country_code):
        self.display_language = display_language

        if salary_data:
            subject_data = salary_data.get('subject', {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label')
            self.subject_welsh = subject_data.get('welsh_label')
            self.aggregate = salary_data.get('agg')
            self.aggregation_year = salary_data.get('aggregation_year')

            self.subject_title_in_local_language = self.subject_english
            if self.display_language == enums.languages.WELSH:
                self.subject_title_in_local_language = self.subject_welsh

            self.unavail_reason = salary_data.get('unavail_reason')
            self.unavailable_reason = ""  # salary_data.get('reason', '')
            self.unavailable_reason_english = salary_data.get('unavail_text_english', '')
            self.unavailable_reason_welsh = salary_data.get('unavail_text_welsh', '')
            self.unavailable_body = self.display_unavailable_info()["reason_body"]

            # Values used by the Earnings partial HTML files to default the DDL to the institution's country.
            #   XF - England
            #   XG - Northern Ireland
            #   XH - Scotland
            #   XI - Wales
            salary_default_country_prov_pc = None

            if institution_country_code == 'XF':
                country_postfix = "_e"
            elif institution_country_code == 'XG':
                country_postfix = "_ni"
                self.is_ni = True
            elif institution_country_code == 'XH':
                country_postfix = "_s"
            elif institution_country_code == 'XI':
                country_postfix = "_w"

            self.resp_rate = None
            if 'resp_rate' in salary_data:
                self.resp_rate = salary_data.get('resp_rate') + "%"

            if salary_data.get("agg"):
                self.pop = salary_data.get('pop')
                self.lq = salary_data.get('lq')
                self.med = salary_data.get('med')
                self.uq = salary_data.get('uq')

                self.prov_pc_uk = salary_data.get('inst_prov_pc_uk')
                self.prov_pc_e = salary_data.get('inst_prov_pc_e')
                self.prov_pc_s = salary_data.get('inst_prov_pc_s')
                self.prov_pc_w = salary_data.get('inst_prov_pc_w')
                self.prov_pc_ni = salary_data.get('inst_prov_pc_ni')

                self.salary_default_country_prov_pc = salary_data.get("inst_prov_pc" + country_postfix)

            if 'inst_prov_pc_nw' in salary_data:
                self.prov_pc_nw = salary_data.get('inst_prov_pc_nw')
                self.prov_pc_ne = salary_data.get('inst_prov_pc_ne')
                self.prov_pc_em = salary_data.get('inst_prov_pc_em')
                self.prov_pc_wm = salary_data.get('inst_prov_pc_wm')
                self.prov_pc_ee = salary_data.get('inst_prov_pc_ee')
                self.prov_pc_se = salary_data.get('inst_prov_pc_se')
                self.prov_pc_sw = salary_data.get('inst_prov_pc_sw')
                self.prov_pc_yh = salary_data.get('inst_prov_pc_yh')
                self.prov_pc_lo = salary_data.get('inst_prov_pc_lo')
                self.prov_pc_ed = salary_data.get('inst_prov_pc_ed')
                self.prov_pc_gl = salary_data.get('inst_prov_pc_gl')
                self.prov_pc_cf = salary_data.get('inst_prov_pc_cf')

            if 'earnings_agg_unavail_message' in salary_data and len(
                    salary_data.get('earnings_agg_unavail_message')) > 0:
                self.earnings_aggregation_msg = {}
                if self.display_language == enums.languages.ENGLISH:
                    self.earnings_aggregation_str = salary_data.get('earnings_agg_unavail_message')['english']
                else:
                    self.earnings_aggregation_str = salary_data.get('earnings_agg_unavail_message')['welsh']
                    self.subject_title_in_local_language = self.subject_welsh

                self.earnings_aggregation_msg["msg_heading"], self.earnings_aggregation_msg[
                    "msg_body"] = separate_unavail_reason(self.earnings_aggregation_str)

                if self.aggregate in ["1", "2", "11", "12", "21", "22"]:
                    header = UNAVAILABLE["new_course_earnings_unavail_header"][self.display_language].format(
                        self.display_subject_name())
                    self.earnings_aggregation_msg["msg_heading"] = header
                    self.earnings_aggregation_msg["msg_body"] = UNAVAILABLE["new_course_earnings_unavail_body"][self.display_language]
                    self.unavailable_reason_welsh = {
                        "header": header,
                        "body": UNAVAILABLE["new_course_earnings_unavail_body"]["cy"]
                    }

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

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english
