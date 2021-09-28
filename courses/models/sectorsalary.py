from CMS import translations
from core.utils import enums
from courses.models.utils import separate_unavail_reason


class SectorSalary:

    def __init__(self, salary_data, display_language, institution_country_code):
        self.display_language = display_language
        self.no_salary_node = "true"

        if salary_data:
            subject_data = salary_data.get('subject', {})
            self.subject_code = subject_data.get('code', '')
            self.subject_english = subject_data.get('english_label', '')
            self.subject_welsh = subject_data.get('welsh_label', '')

            # Values used by the Earnings partial HTML files to default the DDL to the institution's country.
            #   XF - England
            #   XG - Northern Ireland
            #   XH - Scotland
            #   XI - Wales
            self.salary_default_country_med = None
            self.salary_default_country_lq = None
            self.salary_default_country_uq = None
            self.salary_default_country_pop = None
            # salary_default_country_prov_pc = None

            if institution_country_code == 'XF':
                country_postfix = "_e"
                self.country = translations.term_for_key(key="england", language=self.display_language)
            elif institution_country_code == 'XG':
                country_postfix = "_ni"
                self.country = translations.term_for_key(key="northern_ireland", language=self.display_language)
            elif institution_country_code == 'XH':
                country_postfix = "_s"
                self.country = translations.term_for_key(key="scotland", language=self.display_language)
            elif institution_country_code == 'XI':
                country_postfix = "_w"
                self.country = translations.term_for_key(key="wales", language=self.display_language)

            self.no_salary_node = "false"
            if 'lq_uk' in salary_data:
                self.lq_uk = salary_data['lq_uk']
                self.med_uk = salary_data['med_uk']
                self.uq_uk = salary_data['uq_uk']
                self.pop_uk = salary_data['pop_uk']

                self.lq_e = salary_data['lq_e']
                self.med_e = salary_data['med_e']
                self.uq_e = salary_data['uq_e']
                self.pop_e = salary_data['pop_e']

                self.lq_w = salary_data['lq_w']
                self.med_w = salary_data['med_w']
                self.uq_w = salary_data['uq_w']
                self.pop_w = salary_data['pop_w']

                self.lq_s = salary_data['lq_s']
                self.med_s = salary_data['med_s']
                self.uq_s = salary_data['uq_s']
                self.pop_s = salary_data['pop_s']

                # if 'resp_uk' in salary_data:
                #     self.resp_uk = salary_data['resp_uk']
                #     self.resp_e = salary_data['resp_e']
                #     self.resp_w = salary_data['resp_w']
                #     self.resp_s = salary_data['resp_s']

                if "lq" + country_postfix in salary_data:
                    self.salary_default_country_med = salary_data["med" + country_postfix]
                    self.salary_default_country_lq = salary_data["lq" + country_postfix]
                    self.salary_default_country_uq = salary_data["uq" + country_postfix]
                    self.salary_default_country_pop = salary_data["pop" + country_postfix]

            if 'lq_ni' in salary_data:
                self.lq_ni = salary_data['lq_ni']
                self.med_ni = salary_data['med_ni']
                self.uq_ni = salary_data['uq_ni']
                self.pop_ni = salary_data['pop_ni']
                # self.resp_ni = salary_data['resp_ni']

            if 'lq_nw' in salary_data:
                self.lq_nw = salary_data['lq_nw']
                self.med_nw = salary_data['med_nw']
                self.uq_nw = salary_data['uq_nw']
                self.pop_nw = salary_data['pop_nw']

                self.lq_ne = salary_data['lq_ne']
                self.med_ne = salary_data['med_ne']
                self.uq_ne = salary_data['uq_ne']
                self.pop_ne = salary_data['pop_ne']

                self.lq_em = salary_data['lq_em']
                self.med_em = salary_data['med_em']
                self.uq_em = salary_data['uq_em']
                self.pop_em = salary_data['pop_em']

                self.lq_wm = salary_data['lq_wm']
                self.med_wm = salary_data['med_wm']
                self.uq_wm = salary_data['uq_wm']
                self.pop_wm = salary_data['pop_wm']

                self.lq_ee = salary_data['lq_ee']
                self.med_ee = salary_data['med_ee']
                self.uq_ee = salary_data['uq_ee']
                self.pop_ee = salary_data['pop_ee']

                self.lq_se = salary_data['lq_se']
                self.med_se = salary_data['med_se']
                self.uq_se = salary_data['uq_se']
                self.pop_se = salary_data['pop_se']

                self.lq_sw = salary_data['lq_sw']
                self.med_sw = salary_data['med_sw']
                self.uq_sw = salary_data['uq_sw']
                self.pop_sw = salary_data['pop_sw']

                self.lq_yh = salary_data['lq_yh']
                self.med_yh = salary_data['med_yh']
                self.uq_yh = salary_data['uq_yh']
                self.pop_yh = salary_data['pop_yh']

                self.lq_lo = salary_data['lq_lo']
                self.med_lo = salary_data['med_lo']
                self.uq_lo = salary_data['uq_lo']
                self.pop_lo = salary_data['pop_lo']

                self.lq_ed = salary_data['lq_ed']
                self.med_ed = salary_data['med_ed']
                self.uq_ed = salary_data['uq_ed']
                self.pop_ed = salary_data['pop_ed']

                self.lq_gl = salary_data['lq_gl']
                self.med_gl = salary_data['med_gl']
                self.uq_gl = salary_data['uq_gl']
                self.pop_gl = salary_data['pop_gl']

                self.lq_cf = salary_data['lq_cf']
                self.med_cf = salary_data['med_cf']
                self.uq_cf = salary_data['uq_cf']
                self.pop_cf = salary_data['pop_cf']

            self.unavailable_reason_region_not_exists = ""
            self.unavailable_reason_region_not_nation = ""
            self.unavailable_reason_region_is_ni = ""

            self.unavail_text_region_not_exists_english = salary_data['unavail_text_region_not_exists_english']
            self.unavail_text_region_not_exists_welsh = salary_data['unavail_text_region_not_exists_welsh']

            if 'unavail_text_region_not_nation_english' in salary_data:
                self.unavail_text_region_not_nation_english = salary_data['unavail_text_region_not_nation_english']
                self.unavail_text_region_not_nation_welsh = salary_data['unavail_text_region_not_nation_welsh']
            else:
                self.unavail_text_region_not_nation_english = ""
                self.unavail_text_region_not_nation_welsh = ""

            if 'unavail_text_region_is_ni_english' in salary_data:
                self.unavail_text_region_is_ni_english = salary_data['unavail_text_region_is_ni_english']
                self.unavail_text_region_is_ni_welsh = salary_data['unavail_text_region_is_ni_welsh']
            else:
                self.unavail_text_region_is_ni_english = ""
                self.unavail_text_region_is_ni_welsh = ""

    def display_unavailable_info(self, language=enums.languages.ENGLISH):
        if not self.display_language or self.display_language == "":
            self.display_language = language

        unavailable = {}

        if self.unavailable_reason_region_not_exists:
            unavailable["unavailable_region_not_exists"] = self.unavailable_reason_region_not_exists
        else:
            if self.display_language == enums.languages.ENGLISH:
                unavailable[
                    "unavailable_region_not_exists"] = self.unavail_text_region_not_exists_english if self.unavail_text_region_not_exists_english \
                    else self.unavail_text_region_not_exists_welsh
            else:
                unavailable[
                    "unavailable_region_not_exists"] = self.unavail_text_region_not_exists_welsh if self.unavail_text_region_not_exists_welsh else self.unavail_text_region_not_exists_english

        if self.unavailable_reason_region_not_nation:
            unavailable["unavailable_region_not_nation"] = self.unavailable_reason_region_not_nation
        elif hasattr(self, 'unavail_text_region_not_nation_english'):
            if self.display_language == enums.languages.ENGLISH:
                unavailable[
                    "unavailable_region_not_nation"] = self.unavail_text_region_not_nation_english if self.unavail_text_region_not_nation_english \
                    else self.unavail_text_region_not_nation_welsh
            else:
                unavailable[
                    "unavailable_region_not_nation"] = self.unavail_text_region_not_nation_welsh if self.unavail_text_region_not_nation_welsh else self.unavail_text_region_not_nation_english

        if self.unavailable_reason_region_is_ni:
            unavailable["unavailable_region_is_ni"] = self.unavailable_reason_region_is_ni
        elif hasattr(self, 'unavail_text_region_is_ni_english'):
            if self.display_language == enums.languages.ENGLISH:
                unavailable[
                    "unavailable_region_is_ni"] = self.unavail_text_region_is_ni_english if self.unavail_text_region_is_ni_english \
                    else self.unavail_text_region_is_ni_welsh
            else:
                unavailable[
                    "unavailable_region_is_ni"] = self.unavail_text_region_is_ni_welsh if self.unavail_text_region_is_ni_welsh else self.unavail_text_region_is_ni_english

        unavailable["unavailable_region_not_exists_heading"], unavailable[
            "unavailable_region_not_exists_body"] = separate_unavail_reason(
            unavailable["unavailable_region_not_exists"])
        unavailable["unavailable_region_is_ni_heading"], unavailable[
            "unavailable_region_is_ni_body"] = separate_unavail_reason(unavailable["unavailable_region_is_ni"])

        return unavailable
