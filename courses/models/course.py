import json
import logging
from typing import Set

import requests

from CMS import translations
from CMS.enums import enums
from courses import request_handler
from errors.models import ApiError
from institutions.models import InstitutionOverview
from .continuationstatistics import ContinuationStatistics
from .courseaccrediation import CourseAccreditation
from .courseother import CourseDistanceLearning
from .courseother import CourseFoundationYear
from .courseother import CourseLength
from .courseother import CourseLink
from .courseother import CourseLocation
from .coursesubject import CourseSubject
from .employmentstatistics import EmploymentStatistics
from .entrystatistics import EntryStatistics
from .generics import CourseCountry
from .generics import CourseMode
from .generics import CourseQualification
from .generics import CourseSandwichYear
from .generics import CourseYearAbroad
from .graduateperceptionstats import GraduatePerceptionStatistics
from .joblist import JobList
from .jobtypestats import JobTypeStatistics
from .salariesaggregate import SalariesAggregate
from .salary import Salary
from .satisfactionstats import SatisfactionStatistics
from .sectorsalary import SectorSalary
from .tariffstats import TariffStatistics
from .utils import separate_unavail_reason

logger = logging.getLogger(__name__)

class Course:
    MODES = {
        'Full-time': 1,
        'Part-time': 2,
        'FullTime': 1,
        'PartTime': 2,
        'Full time': 1,
        'Part time': 2
    }

    def __init__(self, data_obj, language):
        self.id = data_obj.get('id')
        self.display_language = language
        course_details = data_obj.get('course')
        logger.info(f"course_details {course_details}")
        if course_details:
            self.country = CourseCountry(course_details.get('country'))
            self.kis_course_id = course_details.get('kis_course_id')

            self.data_from_html = translations.term_for_key('data_from_html', self.display_language)
            self.data_from_htlocations_listml_average_earnings_year_range = translations.term_for_key(
                'data_from_html_average_earnings_year_range', self.display_language)

            self.ucas_programme_id = course_details.get('ucas_programme_id')
            self.qualification = CourseQualification(course_details.get('qualification'))

            title = course_details.get('title')
            if title:
                self.english_title = title.get('english', '')
                self.welsh_title = title.get('welsh', '')
            self.honours_award_provision = course_details.get('honours_award_provision')

            institution = course_details.get('institution')
            self.institution = InstitutionOverview(institution, language)
            self.locations = []
            if course_details.get('locations'):
                for location in course_details.get('locations'):
                    self.locations.append(CourseLocation(location, self.display_language))

            self.length = CourseLength(course_details.get('length_of_course'), language)
            self.mode = CourseMode(course_details.get('mode'))
            self.distance_learning = CourseDistanceLearning(course_details.get('distance_learning'),
                                                            self.display_language)
            self.sandwich_year = CourseSandwichYear(course_details.get('sandwich_year'))

            self.subject_names = []
            for subject in course_details.get('subjects'):
                self.subject_names.append(CourseSubject(subject, self.display_language))

            self.year_abroad = CourseYearAbroad(course_details.get('year_abroad'))
            self.foundation_year = CourseFoundationYear(course_details.get('foundation_year_availability'),
                                                        self.display_language)

            self.course_level = course_details.get('course_level')

            stats = course_details.get('statistics')
            if stats:
                self.satisfaction_stats = []
                for satisfaction_stats in stats.get('nss'):
                    self.satisfaction_stats.append(SatisfactionStatistics(satisfaction_stats, self.display_language))
                self.nhs_satisfaction_stats = []
                if stats.get('nhs_nss'):
                    for data_set in stats.get('nhs_nss'):
                        self.nhs_satisfaction_stats.append(SatisfactionStatistics(data_set, self.display_language))
                self.entry_stats = []
                for data_set in stats.get('entry'):
                    self.entry_stats.append(EntryStatistics(data_set, self.display_language))
                self.tariff_stats = []
                for data_set in stats.get('tariff'):
                    self.tariff_stats.append(TariffStatistics(data_set, self.display_language))
                self.continuation_stats = []
                for data_set in stats.get('continuation'):
                    self.continuation_stats.append(ContinuationStatistics(data_set, self.display_language))

                self.employment_stats = []
                for data_set in stats.get('employment'):
                    self.employment_stats.append(EmploymentStatistics(data_set, self.display_language))
                self.job_type_stats = []
                for data_set in stats.get('job_type'):
                    self.job_type_stats.append(JobTypeStatistics(data_set, self.display_language))
                self.job_lists = []
                for data_set in stats.get('job_list'):
                    self.job_lists.append(JobList(data_set, self.display_language))

            self.accreditations = []
            accreditations = course_details.get('accreditations')
            if accreditations:
                for accreditation in accreditations:
                    self.accreditations.append(CourseAccreditation(accreditation, self.display_language))

            self.course_links = self.set_course_links(course_details.get('links'), self.display_language)
            self.overall_satisfaction = self.sync_satisfaction_stats()

            self.in_employment_15_mths = course_details.get('in_employment_15_mths')

            self.graduate_perceptions = []
            for data_set in course_details.get('go_voice_work'):
                self.graduate_perceptions.append(GraduatePerceptionStatistics(data_set, self.display_language))

            # Salary Summary box content.
            # e.g. {15 months} after the course for {Accountancy (non-specific)} graduates at {University of Glasgow}
            # self.summary_med_sal_time summary_med_sal_text_1 self.course_title summary_med_sal_text_2 self.institution
            self.summary_med_sal_value = "no_data"
            self.institution_name = self.institution.pub_ukprn_name
            self.summary_med_sal_sbj = title

            if 'med' in course_details.get('go_salary_inst')[0]:
                self.summary_med_sal_value = course_details.get('go_salary_inst')[0]['med']

                if self.display_language == enums.languages.ENGLISH:
                    self.summary_med_sal_time = "15 months"
                    self.course_title = self.english_title
                    self.summary_med_sal_sbj = course_details.get('go_salary_inst')[0]['subject']['english_label']
                else:
                    self.summary_med_sal_time = "15 mis"
                    self.course_title = self.welsh_title
                    self.summary_med_sal_sbj = course_details.get('go_salary_inst')[0]['subject']['welsh_label']
            elif 'med' in course_details.get('leo3_inst')[0]:
                self.summary_med_sal_value = course_details.get('leo3_inst')[0]['med']
                # self.summary_med_sal_sbj = course_details.get('leo3_inst')[0]['sbj']

                if self.display_language == enums.languages.ENGLISH:
                    self.summary_med_sal_time = "3 years"
                    self.course_title = self.english_title
                    self.summary_med_sal_sbj = course_details.get('leo3_inst')[0]['subject']['english_label']
                else:
                    self.summary_med_sal_time = "3 blynedd"
                    self.course_title = self.welsh_title
                    self.summary_med_sal_sbj = course_details.get('leo3_inst')[0]['subject']['welsh_label']

            self.default_country_postfix = "_uk"
            self.default_region = "The UK"

            if self.country.code == 'XF':
                self.default_country_postfix = "_e"
                self.default_region = "England"
            elif self.country.code == 'XG':
                self.default_country_postfix = "_ni"
                self.default_region = "Northern Ireland"
            elif self.country.code == 'XH':
                self.default_country_postfix = "_s"
                self.default_region = "Scotland"
            elif self.country.code == 'XI':
                self.default_country_postfix = "_w"
                self.default_region = "Wales"

            if language == enums.languages.WELSH:
                with open("./CMS/static/jsonfiles/regions.json", "r") as f:
                    regions = f.read()

                region_dict = json.loads(regions)
                for region_elem in region_dict:
                    elem_name_en = region_elem['name_en']
                    if elem_name_en == self.default_region:
                        self.default_region = region_elem['name_cy']
                        break

            prefix = translations.term_for_key('average_earnings_year_range', language)
            self.go_year_range = prefix + " {}-{}".format(2021, 22)
            self.leo3_year_range = prefix + " {}-{}".format(2014, 16)
            self.leo5_year_range = prefix + " {}-{}".format(2014, 16)

            self.go_salaries_inst = []
            if course_details.get('go_salary_inst'):
                for go_salary_inst in course_details.get('go_salary_inst'):
                    self.go_salaries_inst.append(Salary(go_salary_inst, self.display_language, self.country.code))
            self.leo3_salaries_inst = []
            if course_details.get('leo3_inst'):
                for leo3_salary_inst in course_details.get('leo3_inst'):
                    self.leo3_salaries_inst.append(Salary(leo3_salary_inst, self.display_language, self.country.code))
            self.leo5_salaries_inst = []
            if course_details.get('leo5_inst'):
                for leo5_salary_inst in course_details.get('leo5_inst'):
                    self.leo5_salaries_inst.append(Salary(leo5_salary_inst, self.display_language, self.country.code))

            self.go_salaries_sector = []
            if course_details.get('go_salary_sector'):
                for go_salary_sector in course_details.get('go_salary_sector'):
                    self.go_salaries_sector.append(
                        SectorSalary(go_salary_sector, self.display_language, self.country.code))
            self.leo3_salaries_sector = []
            if course_details.get('leo3_salary_sector'):
                for leo3_salary_sector in course_details.get('leo3_salary_sector'):
                    self.leo3_salaries_sector.append(
                        SectorSalary(leo3_salary_sector, self.display_language, self.country.code))
            self.leo5_salaries_sector = []
            if course_details.get('leo5_salary_sector'):
                for leo5_salary_sector in course_details.get('leo5_salary_sector'):
                    self.leo5_salaries_sector.append(
                        SectorSalary(leo5_salary_sector, self.display_language, self.country.code))

            self.is_ni_provider = course_details.get('country')['code'] == 'XG'

            self.salary_aggregates = []
            for code in self.get_subject_codes_for_earnings_aggregation():
                earnings_aggregate = SalariesAggregate(code, self.display_language, self.is_ni_provider,
                                                       self.mode.label)
                earnings_aggregate.sync_institution_earnings(self.go_salaries_inst)
                earnings_aggregate.sync_institution_earnings(self.leo3_salaries_inst)
                earnings_aggregate.sync_institution_earnings(self.leo5_salaries_inst)
                earnings_aggregate.sync_sector_earnings(self.go_salaries_sector)
                earnings_aggregate.sync_sector_earnings(self.leo3_salaries_sector)
                earnings_aggregate.sync_sector_earnings(self.leo5_salaries_sector)
                self.salary_aggregates.append(earnings_aggregate)

    # This is the message to display at the top level of the Earnings accordion section if no data is available.
    def display_no_earnings_info(self):
        unavailable = {}

        if self.display_language == enums.languages.ENGLISH:
            unavailable[
                "reason"] = "Sorry, there is no data available for this course.\n\nThis may be because the course size is too small. This does not reflect on the quality of the course."
        else:
            unavailable[
                "reason"] = "Yn anffodus, nid oes data ar gael ar gyfer y cwrs hwn.\n\nGall hyn fod oherwydd bod maint y cwrs yn rhy fach. Nid yw hyn yn adlewyrchu ansawdd y cwrs."

        unavailable["reason_heading"], unavailable["reason_body"] = separate_unavail_reason(unavailable["reason"])

        return unavailable

    def display_no_data(self):
        unavailable = {}

        if self.display_language == enums.languages.ENGLISH:
            unavailable[
                "reason"] = "This is because the course has not yet run or has not been running long enough for this data to be available."
        else:
            unavailable[
                "reason"] = "Mae hyn oherwydd nad yw'r cwrs wedi'i gynnal eto neu nid yw wedi cael ei gynnal yn ddigon hir i’r data hwn fod ar gael."

        return unavailable

    def get_subject_codes_for_earnings_aggregation(self):
        subject_codes = []
        all_salaries_inst = self.go_salaries_inst + self.leo3_salaries_inst + self.leo5_salaries_inst
        for element in all_salaries_inst:
            if element.subject_code and element.subject_code not in subject_codes:
                subject_codes.append(element.subject_code)
        return subject_codes

    def set_course_links(self, links, language):
        link_objs = {'course_details': [], 'costs_support': []}
        if enums.uni_link_keys.COURSE in links:
            link_objs.get('course_details').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.COURSE, self.display_language),
                           links.get(enums.uni_link_keys.COURSE),
                           enums.languages_map.get(language)))
        if enums.uni_link_keys.TEACHING_METHODS in links:
            link_objs.get('course_details').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.TEACHING_METHODS, self.display_language),
                           links.get(enums.uni_link_keys.TEACHING_METHODS),
                           enums.languages_map.get(language)))
        if enums.uni_link_keys.ASSESSMENT in links:
            link_objs.get('course_details').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.ASSESSMENT, self.display_language),
                           links.get(enums.uni_link_keys.ASSESSMENT),
                           enums.languages_map.get(language)))
        if enums.uni_link_keys.EMPLOYMENT in links:
            link_objs.get('course_details').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.EMPLOYMENT, self.display_language),
                           links.get(enums.uni_link_keys.EMPLOYMENT),
                           enums.languages_map.get(language)))
        if enums.uni_link_keys.COSTS in links:
            link_objs.get('costs_support').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.COSTS, self.display_language),
                           links.get(enums.uni_link_keys.COSTS),
                           enums.languages_map.get(language)))
        if self.locations and self.locations[0].links and enums.uni_link_keys.ACCOMMODATION in self.locations[0].links:
            link_objs.get('costs_support').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.ACCOMMODATION, self.display_language),
                           self.locations[0].links.get(
                               enums.uni_link_keys.ACCOMMODATION),
                           enums.languages_map.get(language)))
        if enums.uni_link_keys.FINANCIAL_SUPPORT in links:
            link_objs.get('costs_support').append(
                CourseLink(translations.term_for_key(enums.uni_link_keys.FINANCIAL_SUPPORT, self.display_language),
                           links.get(enums.uni_link_keys.FINANCIAL_SUPPORT),
                           enums.languages_map.get(language)))
        return link_objs

    @property
    def number_of_locations(self):
        return len(self.locations)

    @property
    def locations_list(self) -> str:
        location_names = self.all_location_names
        return ', '.join(location_names)

    @property
    def all_location_names(self) -> Set[str]:
        """ returns a list of unique locations"""
        location_names = []
        for location in self.locations:
            if self.display_language == enums.languages.WELSH:
                if location.welsh_name:
                    location_names.append(location.welsh_name)
                else:
                    location_names.append(location.english_name)
            else:
                location_names.append(location.english_name)

        return set(location_names)

    @property
    def has_multiple_subject_names(self):
        return len(self.subject_names) > 1

    @property
    def show_satisfaction_stats(self):
        show_satisfaction_stats = self.satisfaction_stats and self.satisfaction_stats[0].show_satisfaction_stats()
        show_nhs_stats = self.nhs_satisfaction_stats and self.nhs_satisfaction_stats[0].show_nhs_stats()
        return show_satisfaction_stats or show_nhs_stats

    @property
    def has_multiple_satisfaction_stats(self):
        return len(self.overall_satisfaction) > 1

    @property
    def has_multiple_continuation_stats(self):
        return len(self.continuation_stats) > 1

    @property
    def show_entry_information_stats(self):
        show_entry_stats = self.entry_stats and self.entry_stats[0].display_stats
        show_tariff_stats = self.tariff_stats and self.tariff_stats[0].show_stats()

        return show_entry_stats or show_tariff_stats

    @property
    def has_multiple_entry_stats(self):
        return len(self.entry_stats) > 1

    @property
    def has_multiple_tariff_stats(self):
        return len(self.tariff_stats) > 1

    @property
    def show_after_one_year_stats(self):
        return self.continuation_stats and self.continuation_stats[0].display_stats

    @property
    def has_multiple_one_year_stats(self):
        return len(self.continuation_stats) > 1

    @property
    def has_multiple_graduate_perceptions_stats(self):
        return len(self.graduate_perceptions) > 1

    @property
    def has_multiple_employment_stats(self):
        return len(self.employment_stats) > 1

    @property
    def has_multiple_job_type_stats(self):
        return len(self.job_type_stats) > 1

    @property
    def has_multiple_job_lists(self):
        return len(self.job_lists) > 1

    @property
    def has_multiple_salary_aggregates(self):
        return len(self.salary_aggregates) > 1

    @property
    def seo_title(self):
        english = self.display_language == enums.languages.ENGLISH

        if english:
            title = self.english_title if self.english_title else self.welsh_title
        else:
            title = self.welsh_title if self.welsh_title else self.english_title
        at = "at" if english else "yn"
        return f"{title} {at} {self.institution_name}"

    def display_title(self):
        honours = " "
        if int(self.honours_award_provision) == 1:
            honours = " (Hons) "

        english_title = self.qualification.label + honours + self.english_title
        welsh_title = self.qualification.label + honours + self.welsh_title

        if self.display_language == enums.languages.ENGLISH:
            return english_title if self.english_title else welsh_title
        return welsh_title if self.welsh_title else english_title

    @classmethod
    def find(cls, institution_id, course_id, mode, language):
        course = None
        error = None

        response = request_handler.load_course_data(institution_id, course_id, cls.get_mode_code(mode))

        if type(response) == requests.models.Response:
            if response.ok:
                course = cls(response.json(), language)
            else:
                error = ApiError(response.status_code, 'Loading details for course %s %s at %s' %
                                 (course_id, mode, institution_id))
        elif type(response) == dict:
            course = cls(response, language)

        return course, error

    @staticmethod
    def get_mode_code(mode):
        return Course.MODES.get(mode)

    def sync_satisfaction_stats(self):
        overall_satisfaction = []
        for satisfaction_stats in self.satisfaction_stats:
            satisfaction_pair = {'satisfaction_stats': satisfaction_stats, 'nhs_satisfaction_stats': None}
            for nhs_stats in self.nhs_satisfaction_stats:
                if nhs_stats.subject_code == satisfaction_stats.subject_code:
                    satisfaction_pair['nhs_satisfaction_stats'] = nhs_stats
            overall_satisfaction.append(satisfaction_pair)
        return overall_satisfaction

    def sync_occupation_stats(self):
        occupation_stats = []
        if len(self.job_type_stats) == len(self.job_lists):
            occupation_stats = [(jt_stat, jl_stat) for jt_stat in self.job_type_stats for jl_stat in self.job_lists if
                                jt_stat.subject_code == jl_stat.subject_code]
        return occupation_stats
