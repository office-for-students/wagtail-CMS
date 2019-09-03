from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.core import blocks

from CMS.translations import DICT
from CMS.enums import enums

from core.models import DiscoverUniBasePage
from core.utils import fallback_to
from courses import request_handler
from errors.models import ApiError
from institutions.models import InstitutionOverview


STUDENT_SATISFACTION_KEY = 'student_satisfaction'
ENTRY_INFO_KEY = 'entry_information'
AFTER_ONE_YEAR_KEY = 'after_one_year'
AFTER_COURSE_KEY = 'after_the_course'
ACCREDITATION_KEY = 'professional_accreditation'


class AccordionPanel(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)


class SatisfactionDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return STUDENT_SATISFACTION_KEY


class EntryInfoDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return ENTRY_INFO_KEY


class AfterOneYearDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return AFTER_ONE_YEAR_KEY


class AfterCourseDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return AFTER_COURSE_KEY


class AccreditationDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return ACCREDITATION_KEY


class SatisfactionBlock(AccordionPanel):
    lead_text = blocks.CharBlock(required=False)
    intro_body = blocks.RichTextBlock(blank=True)
    teaching_stats_header = blocks.CharBlock(required=False)
    learning_opportunities_stats_header = blocks.CharBlock(required=False)
    assessment_stats_header = blocks.CharBlock(required=False)
    support_stats_header = blocks.CharBlock(required=False)
    organisation_stats_header = blocks.CharBlock(required=False)
    learning_resources_stats_header = blocks.CharBlock(required=False)
    learning_community_stats_header = blocks.CharBlock(required=False)
    student_voice_stats_header = blocks.CharBlock(required=False)
    nhs_placement_stats_header = blocks.CharBlock(required=False)
    data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = SatisfactionDataSet


class EntryInformationBlock(AccordionPanel):
    qualification_heading = blocks.CharBlock(required=False)
    qualification_intro = blocks.CharBlock(required=False)
    qualification_label_explanation_heading = blocks.CharBlock(required=False)
    qualification_label_explanation_body = blocks.RichTextBlock(blank=True)
    qualification_data_source = blocks.RichTextBlock(blank=True)

    tariffs_heading = blocks.CharBlock(required=False)
    tariffs_intro = blocks.CharBlock(required=False)
    tariffs_data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EntryInfoDataSet


class AfterOneYearBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)
    intro = blocks.CharBlock(required=False)
    lead = blocks.CharBlock(required=False)
    label_explanation_heading = blocks.CharBlock(required=False)
    label_explanation_body = blocks.RichTextBlock(blank=True)
    data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = AfterOneYearDataSet


class AfterCourseBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)
    intro = blocks.RichTextBlock(blank=True)

    six_month_earnings_heading = blocks.CharBlock(required=False)
    six_month_earnings_explanation = blocks.RichTextBlock(blank=True)
    six_month_earnings_salary_range_heading = blocks.CharBlock(required=False)
    six_month_earnings_data_source = blocks.RichTextBlock(blank=True)

    three_years_earnings_heading = blocks.CharBlock(required=False)
    three_years_earnings_explanation = blocks.RichTextBlock(blank=True)
    three_years_earnings_salary_range_heading = blocks.CharBlock(required=False)
    three_years_earnings_data_source = blocks.RichTextBlock(blank=True)

    six_month_employment_heading = blocks.CharBlock(required=False)
    six_month_employment_intro = blocks.CharBlock(required=False)
    six_month_employment_lead = blocks.CharBlock(required=False)
    six_month_employment_data_source = blocks.RichTextBlock(blank=True)

    six_month_employment_roles_heading = blocks.CharBlock(required=False)
    six_month_employment_roles_intro = blocks.CharBlock(required=False)
    six_month_employment_roles_label_explanation_heading = blocks.CharBlock(required=False)
    six_month_employment_roles_label_explanation_body = blocks.RichTextBlock(blank=True)
    six_month_employment_roles_data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = AfterCourseDataSet


class AccreditationBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)

    class Meta:
        value_class = AccreditationDataSet


class CourseDetailPage(DiscoverUniBasePage):
    accordions = StreamField([
        ('satisfaction_panel', SatisfactionBlock(required=True, icon='collapse-down')),
        ('entry_information_panel', EntryInformationBlock(required=True, icon='collapse-down')),
        ('after_one_year_panel', AfterOneYearBlock(required=True, icon='collapse-down')),
        ('after_course_panel', AfterCourseBlock(required=True, icon='collapse-down')),
        ('accreditation_panel', AccreditationBlock(required=True, icon='collapse-down'))
    ])
    uni_site_links_header = TextField(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('accordions'),
        FieldPanel('uni_site_links_header'),
    ]


class Course:
    MODES = {
        'Full-time': 1,
        'Part-time': 2,
        'FullTime': 1,
        'PartTime': 2
    }

    def __init__(self, data_obj, language):
        self.id = data_obj.get('id')
        self.display_language = language
        course_details = data_obj.get('course')
        if course_details:
            self.country = CourseCountry(course_details.get('country'))
            self.kis_course_id = course_details.get('kis_course_id')
            self.ucas_programme_id = course_details.get('ucas_programme_id')
            self.qualification = CourseQualification(course_details.get('qualification'))

            title = course_details.get('title')
            if title:
                self.english_title = fallback_to(title.get('english'), '')
                self.welsh_title = fallback_to(title.get('welsh'), '')
            self.honours_award_provision = course_details.get('honours_award_provision')

            self.institution = InstitutionOverview(course_details.get('institution'))
            self.locations = []
            if course_details.get('locations'):
                for location in course_details.get('locations'):
                    self.locations.append(CourseLocation(location, self.display_language))

            self.length = CourseLength(course_details.get('length_of_course'), language)
            self.mode = CourseMode(course_details.get('mode'))
            self.distance_learning = CourseDistanceLearning(course_details.get('distance_learning'),
                                                            self.display_language)
            self.sandwich_year = CourseSandwichYear(course_details.get('sandwich_year'))
            self.year_abroad = CourseYearAbroad(course_details.get('year_abroad'))
            self.foundation_year = CourseFoundationYear(course_details.get('foundation_year_availability'),
                                                        self.display_language)

            stats = course_details.get('statistics')
            if stats:
                self.satisfaction_stats = SatisfactionStatistics(stats.get('nss')[0])
                if stats.get('nhs_nss')[0]:
                    self.nhs_satisfaction_stats = SatisfactionStatistics(stats.get('nhs_nss')[0])
                self.entry_stats = []
                for data_set in stats.get('entry'):
                    self.entry_stats.append(EntryStatistics(data_set, self.display_language))
                self.tariff_stats = []
                for data_set in stats.get('tariff'):
                    self.tariff_stats.append(TariffStatistics(data_set, self.display_language))
                self.continuation_stats = []
                for data_set in stats.get('continuation'):
                    self.continuation_stats.append(ContinuationStatistics(data_set, self.display_language))
                self.salary_stats = []
                for data_set in stats.get('salary'):
                    self.salary_stats.append(SalaryStatistics(data_set, self.display_language, title))
                self.employment_stats = EmploymentStatistics(stats.get('employment')[0])
                self.leo_stats = LEOStatistics(stats.get('leo')[0], self.display_language)
                self.job_type_stats = JobTypeStatistics(stats.get('job_type')[0])

            self.accreditations = []
            accreditations = course_details.get('accreditations')
            if accreditations:
                for accreditation in accreditations:
                    self.accreditations.append(CourseAccreditation(accreditation, self.display_language))

            self.course_links = self.set_course_links(course_details.get('links'), self.display_language)

    def set_course_links(self, links, language):
        link_objs = {'course_details': [], 'costs_support': []}
        if enums.uni_link_keys.COURSE in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.COURSE).get(language),
                                                   links.get(enums.uni_link_keys.COURSE),
                                                   enums.languages_map.get(language)))
        if enums.uni_link_keys.TEACHING_METHODS in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.TEACHING_METHODS).get(language),
                                        links.get(enums.uni_link_keys.TEACHING_METHODS),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.ASSESSMENT in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.ASSESSMENT).get(language),
                                                   links.get(enums.uni_link_keys.ASSESSMENT),
                                                   enums.languages_map.get(language)))
        if enums.uni_link_keys.EMPLOYMENT in links:
            link_objs.get('course_details').append(CourseLink(DICT.get(enums.uni_link_keys.EMPLOYMENT).get(language),
                                                   links.get(enums.uni_link_keys.EMPLOYMENT),
                                                   enums.languages_map.get(language)))
        if enums.uni_link_keys.COSTS in links:
            link_objs.get('costs_support').append(CourseLink(DICT.get(enums.uni_link_keys.COSTS).get(language),
                                                  links.get(enums.uni_link_keys.COSTS),
                                                  enums.languages_map.get(language)))
        if self.locations and enums.uni_link_keys.ACCOMMODATION in self.locations[0].links:
            link_objs.get('costs_support').append(CourseLink(DICT.get(enums.uni_link_keys.ACCOMMODATION).get(language),
                                                  self.locations[0].links.get(enums.uni_link_keys.ACCOMMODATION),
                                                  enums.languages_map.get(language)))
        if enums.uni_link_keys.FINANCIAL_SUPPORT in links:
            link_objs.get('costs_support').append(CourseLink(DICT.get(enums.uni_link_keys.FINANCIAL_SUPPORT).get(language),
                                                  links.get(enums.uni_link_keys.FINANCIAL_SUPPORT),
                                                  enums.languages_map.get(language)))
        return link_objs

    @property
    def number_of_locations(self):
        return len(self.locations)

    @property
    def locations_list(self):
        location_names = []
        for location in self.locations:
            location_names.append(location.english_name)
        return ', '.join(location_names)

    @property
    def show_satisfaction_stats(self):
        return self.satisfaction_stats.show_satisfaction_stats() or self.nhs_satisfaction_stats.show_nhs_stats()

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
    def show_after_course_stats(self):
        show_salary_stats = self.salary_stats and self.salary_stats[0].display_stats
        return self.employment_stats.display_stats or self.job_type_stats.display_stats or \
            show_salary_stats or self.show_leo

    @property
    def show_salary_lead(self):
        show_salary_stats = self.salary_stats and self.salary_stats[0].display_stats
        return show_salary_stats or self.show_leo

    @property
    def has_multiple_salary_stats(self):
        return len(self.salary_stats) > 1

    @property
    def show_leo(self):
        return self.country.name == 'England' and self.leo_stats.display_stats

    def display_title(self):
        honours = ""
        if int(self.honours_award_provision) == 1:
            honours = "(Hons) "

        english_title = self.qualification.label + " " + honours + self.english_title
        welsh_title = self.qualification.label + " " + honours + self.welsh_title

        if self.display_language == enums.languages.ENGLISH:
            return english_title if self.english_title else welsh_title
        return welsh_title if self.welsh_title else english_title

    @classmethod
    def find(cls, institution_id, course_id, mode, language):
        course = None
        error = None

        response = request_handler.load_course_data(institution_id, course_id, cls.get_mode_code(mode))

        if response.ok:
            course = cls(response.json(), language)
        else:
            error = ApiError(response.status_code, 'Loading details for course %s %s at %s' %
                             (course_id, mode, institution_id))

        return course, error

    @staticmethod
    def get_mode_code(mode):
        return Course.MODES.get(mode)


class CourseCountry:

    def __init__(self, data_obj):
        if data_obj:
            self.name = fallback_to(data_obj.get('name'), '')
            self.code = data_obj.get('code')


class CourseDistanceLearning:

    def __init__(self, data_obj, language):
        self.display_language = language
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')

    def display_label(self):
        if self.code is not None and str(self.code) in DICT.get('distance_learning_values'):
            return DICT.get('distance_learning_values').get(str(self.code)).get(self.display_language)
        return DICT.get('unknown').get(self.display_language)


class CourseFoundationYear:

    def __init__(self, data_obj, language):
        self.label = DICT.get('unknown').get(language)
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')


class CourseLength:

    def __init__(self, data_obj, language):
        self.label = 0
        if data_obj:
            self.code = data_obj.get('code')
            self.label = fallback_to(data_obj.get('label'), '')


class CourseLink:

    def __init__(self, name, link_obj, language_key):
        self.label = name
        if language_key in link_obj:
            self.link = link_obj.get(language_key)
        else:
            self.link = fallback_to(link_obj.get(enums.languages_full.ENGLISH), '')


class CourseLocation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.latitude = data_obj.get('latitude')
        self.longitude = data_obj.get('longitude')
        name = data_obj.get('name')
        if name:
            self.english_name = fallback_to(name.get('english'), '')
            self.welsh_name = fallback_to(name.get('welsh'), '')
        self.links = data_obj.get('links')

    def display_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.english_name if self.english_name else self.welsh_name
        else:
            return self.welsh_name if self.welsh_name else self.english_name


class CourseMode:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseQualification:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseSandwichYear:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


class CourseYearAbroad:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = fallback_to(data_obj.get('label'), '')


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

            unavailable_data = data_obj.get('unavailable')
            if unavailable_data:
                self.unavailable_code = unavailable_data.get('code')
                self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english


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

            unavailable_data = data_obj.get('unavailable')
            if unavailable_data:
                self.unavailable_code = unavailable_data.get('code')
                self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')

    @property
    def continuing_or_complete(self):
        return self.continuing + self.gained

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english


class EmploymentStatistics:

    def __init__(self, data_obj):
        self.display_stats = False
        self.aggregation_level = 0
        self.unemployed = 0
        self.in_study = 0
        self.in_work = 0
        self.in_work_and_study = 0
        self.in_work_or_study = 0
        self.not_available_for_work_or_study = 0
        self.number_of_students = 0
        self.response_rate = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['assumed_to_be_unemployed', 'in_study', 'in_work',
                                                                 'in_work_and_study', 'in_work_or_study',
                                                                 'not_available_for_work_or_study',
                                                                 'number_of_students', 'response_rate'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.unemployed = fallback_to(data_obj.get('assumed_to_be_unemployed'), 0)
            self.in_study = fallback_to(data_obj.get('in_study'), 0)
            self.in_work = fallback_to(data_obj.get('in_work'), 0)
            self.in_work_and_study = fallback_to(data_obj.get('in_work_and_study'), 0)
            self.in_work_or_study = fallback_to(data_obj.get('in_work_or_study'), 0)
            self.not_available_for_work_or_study = fallback_to(data_obj.get('not_available_for_work_or_study'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_students'), 0)
            self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'
            unavailable_data = data_obj.get('unavailable')
            if unavailable_data:
                self.unavailable_code = unavailable_data.get('code')
                self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')

    @property
    def work_and_or_study(self):
        return self.in_work_or_study


class JobTypeStatistics:

    def __init__(self, data_obj):
        self.display_stats = False
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

            unavailable_data = data_obj.get('unavailable')
            if unavailable_data:
                self.unavailable_code = unavailable_data.get('code')
                self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')


class SalaryStatistics:

    def __init__(self, data_obj, language, course_title):
        self.display_stats = False
        self.display_language = language
        self.aggregation_level = 0
        self.higher_quartile = 0
        self.lower_quartile = 0
        self.median = 0
        self.sector_higher_quartile = 0
        self.sector_lower_quartile = 0
        self.sector_median = 0
        self.number_of_students = 0
        self.response_rate = 0
        self.subject_english_label = ''
        self.subject_welsh_label = ''

        if data_obj:
            self.display_stats = all(key in data_obj for key in ['higher_quartile', 'lower_quartile', 'median',
                                                                 'sector_higher_quartile', 'sector_lower_quartile',
                                                                 'sector_median', 'number_of_graduates',
                                                                 'response_rate'])

            self.aggregation_level = data_obj.get('aggregation_level')
            self.higher_quartile = fallback_to(data_obj.get('higher_quartile'), 0)
            self.lower_quartile = fallback_to(data_obj.get('lower_quartile'), 0)
            self.median = fallback_to(data_obj.get('median'), 0)
            self.sector_higher_quartile = fallback_to(data_obj.get('sector_higher_quartile'), 0)
            self.sector_lower_quartile = fallback_to(data_obj.get('sector_lower_quartile'), 0)
            self.sector_median = fallback_to(data_obj.get('sector_median'), 0)
            self.number_of_students = fallback_to(data_obj.get('number_of_graduates'), 0)
            self.response_rate = str(fallback_to(data_obj.get('response_rate'), 0)) + '%'

            subject = data_obj.get('subject')
            if subject:
                self.subject_code = subject.get('code')
                self.subject_english_label = fallback_to(subject.get("english_label"), '')
                self.subject_welsh_label = fallback_to(subject.get("welsh_label"), '')
            elif course_title:
                self.subject_english_label = fallback_to(course_title.get("english"), '')
                self.subject_welsh_label = fallback_to(course_title.get("welsh"), '')
            else:
                self.subject_english_label = ''
                self.subject_welsh_label = ''

            unavailable_data = data_obj.get('unavailable')
            if unavailable_data:
                self.unavailable_code = unavailable_data.get('code')
                self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')

    def display_subject_label(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english_label if self.subject_english_label else self.subject_welsh_label
        return self.subject_welsh_label if self.subject_welsh_label else self.subject_english_label


class LEOStatistics:

    def __init__(self, data_obj, language):
        self.display_stats = False
        self.display_language = language
        self.subject_english_label = ''
        self.subject_welsh_label = ''
        self.aggregation_level = 0
        self.higher_quartile = 0
        self.lower_quartile = 0
        self.median = 0
        self.number_of_graduates = 0

        if data_obj:
            self.display_stats = all(key in data_obj for key in ["aggregation_level", "higher_quartile",
                                                                 "lower_quartile", "median", "number_of_graduates"])

            self.aggregation_level = data_obj.get("aggregation_level")
            self.higher_quartile = fallback_to(data_obj.get("higher_quartile"), 0)
            self.lower_quartile = fallback_to(data_obj.get("lower_quartile"), 0)
            self.median = fallback_to(data_obj.get("median"), 0)
            self.number_of_graduates = fallback_to(data_obj.get("number_of_graduates"), 0)

            subject = data_obj.get('subject')
            if subject:
                self.subject_code = subject.get('code')
                self.subject_english_label = fallback_to(subject.get("english_label"), '')
                self.subject_welsh_label = fallback_to(subject.get("welsh_label"), '')

            self.unavailable_reason = None
            unavailable_data = data_obj.get('unavailable')
            if unavailable_data:
                self.unavailable_code = unavailable_data.get('code')
                self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')

    def display_subject_label(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english_label if self.subject_english_label else self.subject_welsh_label
        return self.subject_welsh_label if self.subject_welsh_label else self.subject_english_label


class SatisfactionStatistics:

    def __init__(self, data_obj):
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
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = fallback_to(unavailable_data.get('reason'), '')

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


class SatisfactionQuestion:

    def __init__(self, question_data):
        self.show_data_point = False
        if question_data:
            self.show_data_point = 'agree_or_strongly_agree' in question_data
            self.description = fallback_to(question_data.get('description'), '')
            self.agree_or_strongly_agree = fallback_to(question_data.get('agree_or_strongly_agree'), 0)


class TariffStatistics:

    def __init__(self, tariff_data, display_language):
        self.display_language = display_language
        self.tariffs = []

        if tariff_data:
            self.aggregation = tariff_data.get('aggregation')
            self.number_of_students = fallback_to(tariff_data.get('number_of_students'), 0)
            if tariff_data.get('tariffs'):
                for tariff in tariff_data.get('tariffs'):
                    self.tariffs.append(Tariff(tariff))
            self.tariffs.reverse()

            subject_data = tariff_data.get('subject')
            if subject_data:
                self.subject_code = subject_data.get('code')
                self.subject_english = subject_data.get('english_label')
                self.subject_welsh = subject_data.get('welsh_label')

    def show_stats(self):
        return self.tariffs

    def display_subject_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.subject_english if self.subject_english else self.subject_welsh
        return self.subject_welsh if self.subject_welsh else self.subject_english


class Tariff:
    LABELS = {
        "T001": "< 48",
        "T048": "48 - 63",
        "T064": "64 - 79",
        "T080": "80 - 95",
        "T096": "96 - 111",
        "T112": "112 - 127",
        "T128": "128 - 143",
        "T144": "144 - 159",
        "T160": "160 - 175",
        "T176": "176 - 191",
        "T192": "192 - 207",
        "T208": "208 - 223",
        "T224": "224 - 239",
        "T240": "240 <",
    }

    def __init__(self, tariff):
        self.code = tariff.get('code')
        self.description = fallback_to(tariff.get('description'), '')
        self.entrants = fallback_to(tariff.get('entrants'), 0)

    @property
    def label(self):
        if self.code:
            return self.LABELS[self.code]
        return ''


class CourseAccreditation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.type = fallback_to(data_obj.get("type"), '')
        self.accreditor_url = fallback_to(data_obj.get('accreditor_url'), '')
        text = data_obj.get('text')
        if text:
            self.text_english = fallback_to(text.get('english'), '')
            self.text_welsh = fallback_to(text.get('welsh'), '')

        url = data_obj.get('url')
        self.url_english = ''
        self.url_welsh = ''
        if url:
            self.url_english = fallback_to(url.get('english'), '')
            self.url_welsh = fallback_to(url.get('welsh'), '')

        dependent = data_obj.get('dependent_on')
        if dependent:
            self.dependent_on_code = dependent.get('code')
            self.dependent_on_label = fallback_to(dependent.get('label'), '')

    def display_text(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.text_english if self.text_english else self.text_welsh
        return self.text_welsh if self.text_welsh else self.text_english

    def language_url(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.url_english if self.url_english else self.url_welsh
        return self.url_welsh if self.url_welsh else self.url_english

    def show_dependency(self):
        return self.dependent_on_code == '1'
