from CMS.enums import enums
from CMS.translations import DICT
from .salary import Salary
from .sectorsalary import SectorSalary
from .utils import separate_unavail_reason


class SalariesAggregate:
    def __init__(self, subject_code, display_language, is_ni_provider, mode):
        self.mode = mode
        self.subject_code = subject_code
        self.subject_code_one_level_down = self.get_cah_code_for_level(enums.subject_code_levels.ONE_DOWN)
        self.subject_code_two_levels_down = self.get_cah_code_for_level(enums.subject_code_levels.TWO_DOWN)
        self.is_ni_provider = is_ni_provider

        self.display_language = display_language
        self.subject_english = ""
        self.subject_welsh = ""

        self.aggregated_salaries_inst = []
        self.aggregated_salaries_sector = []

    def get_cah_code_for_level(self, level):
        subject_codes = self.subject_code.split("-")
        return "-".join(code_element for code_index, code_element in enumerate(subject_codes) if code_index < level)

    def sync_institution_earnings(self, salaries_inst):
        salary_institution = self.sync_earnings_data(salaries_inst)
        if not salary_institution:
            unavail_text_en = ""
            unavail_text_cy = ""

            if salaries_inst and len(salaries_inst) > 0 and salaries_inst[0].unavailable_reason_english:
                unavail_text_en = salaries_inst[0].unavailable_reason_english
            if salaries_inst and len(salaries_inst) > 0 and salaries_inst[0].unavailable_reason_welsh:
                unavail_text_cy = salaries_inst[0].unavailable_reason_welsh

            salary_institution = self.generate_empty_institution_salary_with_unavail_reason(unavail_text_en,
                                                                                            unavail_text_cy)

        self.aggregated_salaries_inst.append(salary_institution)

    def sync_sector_earnings(self, salaries_sector):
        salary_sector = self.sync_earnings_data(salaries_sector)
        if not salary_sector:
            unavail_text_en = ""
            unavail_text_cy = ""

            if salaries_sector and len(salaries_sector) > 0 and salaries_sector[
                0].unavail_text_region_not_exists_english:
                unavail_text_en = salaries_sector[0].unavail_text_region_not_exists_english
            if salaries_sector and len(salaries_sector) > 0 and salaries_sector[0].unavail_text_region_not_exists_welsh:
                unavail_text_cy = salaries_sector[0].unavail_text_region_not_exists_welsh

            salary_sector = self.generate_empty_sector_salary_with_unavail_reason(unavail_text_en, unavail_text_cy)

        self.aggregated_salaries_sector.append(salary_sector)

    def generate_empty_institution_salary_with_unavail_reason(self, unavail_text_en, unavail_text_cy):
        salary_substitute = Salary(None, self.display_language, None)
        salary_substitute.unavail_reason = "1"
        salary_substitute.unavailable_reason = ""
        salary_substitute.prov_pc_uk = ""
        salary_substitute.prov_pc_e = ""
        salary_substitute.prov_pc_s = ""
        salary_substitute.prov_pc_w = ""
        salary_substitute.prov_pc_ni = ""
        salary_substitute.prov_pc_nw = ""
        salary_substitute.prov_pc_ne = ""
        salary_substitute.prov_pc_em = ""
        salary_substitute.prov_pc_wm = ""
        salary_substitute.prov_pc_ee = ""
        salary_substitute.prov_pc_se = ""
        salary_substitute.prov_pc_sw = ""
        salary_substitute.prov_pc_yh = ""
        salary_substitute.prov_pc_lo = ""
        salary_substitute.prov_pc_ed = ""
        salary_substitute.prov_pc_gl = ""
        salary_substitute.prov_pc_cf = ""

        # TODO: read these values from the course JSON.
        salary_substitute.unavailable_reason_region_not_nation_english = "No data available\n\nSorry, this data is not available at this level."
        salary_substitute.unavailable_reason_region_not_nation_welsh = "Nid oes data ar gael\n\nNid yw'r data hwn ar gael ar gyfer y lefel hon."
        salary_substitute.unavailable_reason_region_is_ni_english = "No data available\n\nSorry, this data is not available for courses in Northern Ireland."
        salary_substitute.unavailable_reason_region_is_ni_welsh = "Nid oes data ar gael\n\nYn anffodus, nid yw'r data hwn ar gael ar gyfer cyrsiau yng Ngogledd Iwerddon."

        if unavail_text_en == "":
            salary_substitute.unavail_text_region_not_exists_english = "No data available\n\nThis is because the course has not yet run or has not been running long enough for this data to be available."
        else:
            salary_substitute.unavail_text_region_not_exists_english = unavail_text_en

        if unavail_text_cy == "":
            salary_substitute.unavail_text_region_not_exists_welsh = "Nid oes data ar gael\n\nMae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael."
        else:
            salary_substitute.unavail_text_region_not_exists_welsh = unavail_text_cy

        if self.is_ni_provider:
            salary_substitute.unavailable_reason_english = salary_substitute.unavailable_reason_region_is_ni_english
            salary_substitute.unavailable_reason_welsh = salary_substitute.unavailable_reason_region_is_ni_welsh
        else:
            salary_substitute.unavailable_reason_english = salary_substitute.unavail_text_region_not_exists_english
            salary_substitute.unavailable_reason_welsh = salary_substitute.unavail_text_region_not_exists_welsh

        # salary_substitute.unavailable_reason_region_not_exists = ""
        return salary_substitute

    def generate_empty_sector_salary_with_unavail_reason(self, unavail_text_en, unavail_text_cy):
        salary_substitute = SectorSalary(None, self.display_language, None)
        salary_substitute.unavail_reason = "1"
        salary_substitute.unavailable_reason = ""

        # TODO: read these values from the course JSON.
        salary_substitute.unavailable_reason_region_not_nation_english = "No data available\n\nSorry, this data is not available at this level."
        salary_substitute.unavailable_reason_region_not_nation_welsh = "Nid oes data ar gael\n\nNid yw'r data hwn ar gael ar gyfer y lefel hon."
        salary_substitute.unavailable_reason_region_is_ni_english = "No data available\n\nSorry, this data is not available for Northern Ireland."
        salary_substitute.unavailable_reason_region_is_ni_welsh = "Nid oes data ar gael\n\nYn anffodus, nid yw’r data hwn ar gael ar gyfer Gogledd Iwerddon."

        if unavail_text_en == "":
            salary_substitute.unavail_text_region_not_exists_english = "No data available\n\nThis is because the course has not yet run or has not been running long enough for this data to be available."
        else:
            salary_substitute.unavail_text_region_not_exists_english = unavail_text_en

        if unavail_text_cy == "":
            salary_substitute.unavail_text_region_not_exists_welsh = "Nid oes data ar gael\n\nMae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael."
        else:
            salary_substitute.unavail_text_region_not_exists_welsh = unavail_text_cy

        if self.display_language == enums.languages.ENGLISH:
            salary_substitute.unavailable_reason_region_not_exists = salary_substitute.unavail_text_region_not_exists_english
            salary_substitute.unavailable_reason_region_not_nation = salary_substitute.unavailable_reason_region_not_nation_english
            salary_substitute.unavailable_reason_region_is_ni = salary_substitute.unavailable_reason_region_is_ni_english
        else:
            salary_substitute.unavailable_reason_region_not_exists = salary_substitute.unavail_text_region_not_exists_welsh
            salary_substitute.unavailable_reason_region_not_nation = salary_substitute.unavailable_reason_region_not_nation_welsh
            salary_substitute.unavailable_reason_region_is_ni = salary_substitute.unavailable_reason_region_is_ni_welsh

        return salary_substitute

    def sync_earnings_data(self, salaries):
        matched_element = None
        for salary_data in salaries:
            if self.matches_subject_code(salary_data.subject_code):
                self.set_when_empty_subject_names(salary_data)
                return salary_data
        for salary_data in salaries:
            if self.matches_subject_code_one_level_down(salary_data.subject_code):
                self.set_when_empty_subject_names(salary_data)
                return salary_data
        for salary_data in salaries:
            if self.matches_subject_code_two_levels_down(salary_data.subject_code):
                self.set_when_empty_subject_names(salary_data)
                return salary_data
        return matched_element

    def matches_subject_code(self, code):
        return code == self.subject_code

    def matches_subject_code_one_level_down(self, code):
        return code == self.subject_code_one_level_down

    def matches_subject_code_two_levels_down(self, code):
        return code == self.subject_code_two_levels_down

    def set_when_empty_subject_names(self, data):
        if not self.subject_english:
            self.subject_english = data.subject_english
        if not self.subject_welsh:
            self.subject_welsh = data.subject_welsh

    def display_subject_name(self):
        mode = self.mode.lower()

        if self.display_language == enums.languages.ENGLISH:
            subject_name = mode + " " + self.subject_english if self.subject_english else self.subject_welsh + " " + mode
        else:
            if mode == "full-time":
                mode = DICT.get('full_time').get(self.display_language).lower()
            elif mode == "part-time":
                mode = DICT.get('part_time').get(self.display_language).lower()

            subject_name = self.subject_welsh + " " + mode if self.subject_welsh else mode + " " + self.subject_english
        return subject_name

    def display_subject_name_earnings_tabs(self):
        mode = self.mode.lower()

        if self.display_language == enums.languages.ENGLISH:
            subject_name = self.subject_english if self.subject_english else self.subject_welsh
        else:
            subject_name = self.subject_welsh if self.subject_welsh else self.subject_english
        return subject_name

    def display_no_data_info(self):
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
