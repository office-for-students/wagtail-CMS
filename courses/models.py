from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.core import blocks

from CMS.translations import DICT
from CMS.enums import enums

from core.models import DiscoverUniBasePage
from courses import request_handler
from errors.models import ApiError
from institutions.models import InstitutionOverview


class AccordionPanel(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)


class SatisfactionDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return 'student_satisfaction'


class EntryInfoDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return 'entry_information'


class AfterOneYearDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return 'after_one_year'


class AfterCourseDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return 'after_the_course'


class AccreditationDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return 'professional_accreditation'


class SatisfactionBlock(AccordionPanel):
    lead_text = blocks.CharBlock(required=False)
    intro_body = blocks.RichTextBlock(blank=True)
    teaching_stats_header = blocks.CharBlock(required=False)
    learning_opportunities_stats_header = blocks.CharBlock(required=False)
    assessment_stats_header = blocks.CharBlock(required=False)
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
        'Part-time': 2
    }

    def __init__(self, data_obj, language):
        self.id = data_obj.get('id')
        self.display_language = language
        course_details = data_obj.get('course')
        if course_details:
            self.country = CourseCountry(course_details.get('country'))
            self.distance_learning = CourseDistanceLearning(course_details.get('distance_learning'),
                                                            self.display_language)
            self.foundation_year = CourseFoundationYear(course_details.get('foundation_year_availability'))
            self.honours_award_provision = course_details.get('honours_award_provision')
            self.institution = InstitutionOverview(course_details.get('institution'))
            self.kis_course_id = course_details.get('kis_course_id')
            self.length = CourseLength(course_details.get('length_of_course'))
            self.locations = []
            if course_details.get('locations'):
                for location in course_details.get('locations'):
                    self.locations.append(CourseLocation(location, self.display_language))
            self.mode = CourseMode(course_details.get('mode'))
            self.qualification = CourseQualification(course_details.get('qualification'))
            self.sandwich_year = CourseSandwichYear(course_details.get('sandwich_year'))
            title = course_details.get('title')
            if title:
                self.english_title = title.get('english')
                self.welsh_title = title.get('welsh')
            self.ucas_programme_id = course_details.get('ucas_programme_id')
            self.year_abroad = CourseYearAbroad(course_details.get('year_abroad'))
            self.accreditations = []
            accreditations = course_details.get('accreditations')
            if accreditations:
                for accreditation in accreditations:
                    self.accreditations.append(CourseAccreditation(accreditation, self.display_language))
            stats = course_details.get('statistics')
            self.entry_stats = EntryStatistics(stats.get('entry')[0])
            self.continuation_stats = ContinuationStatistics(stats.get('continuation')[0])
            self.employment_stats = EmploymentStatistics(stats.get('employment')[0])
            self.job_type_stats = JobTypeStatistics(stats.get('job_type')[0])
            self.salary_stats = SalaryStatistics(stats.get('salary')[0], self.display_language, title)
            self.satisfaction_stats = SatisfactionStatistics(stats.get('nss')[0])
            if stats.get('nhs_nss')[0]:
                self.nhs_satisfaction_stats = SatisfactionStatistics(stats.get('nhs_nss')[0])
            self.tariff_stats = TariffStatistics(stats.get('tariff')[0])
            self.leo_stats = LEOStatistics(stats.get('leo')[0], self.display_language)
            self.course_links = self.set_course_links(course_details.get('links'), self.display_language)

    def set_course_links(self, links, language):
        link_objs = []
        if enums.uni_link_keys.COURSE in links:
            link_objs.append(CourseLink(DICT.get(enums.uni_link_keys.COURSE).get(language),
                                        links.get(enums.uni_link_keys.COURSE),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.TEACHING_METHODS in links:
            link_objs.append(CourseLink(DICT.get(enums.uni_link_keys.TEACHING_METHODS).get(language),
                                        links.get(enums.uni_link_keys.TEACHING_METHODS),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.ASSESSMENT in links:
            link_objs.append(CourseLink(DICT.get(enums.uni_link_keys.ASSESSMENT).get(language),
                                        links.get(enums.uni_link_keys.ASSESSMENT),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.COSTS in links:
            link_objs.append(CourseLink(DICT.get(enums.uni_link_keys.COSTS).get(language),
                                        links.get(enums.uni_link_keys.COSTS),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.ACCOMMODATION in self.locations[0].links:
            link_objs.append(CourseLink(DICT.get(enums.uni_link_keys.ACCOMMODATION).get(language),
                                        self.locations[0].links.get(enums.uni_link_keys.ACCOMMODATION),
                                        enums.languages_map.get(language)))
        if enums.uni_link_keys.FINANCIAL_SUPPORT in links:
            link_objs.append(CourseLink(DICT.get(enums.uni_link_keys.FINANCIAL_SUPPORT).get(language),
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
    def show_leo(self):
        return self.country.name == 'England' and self.leo_stats.unavailable_reason

    def display_title(self):
        honours = ""
        if int(self.honours_award_provision) == 1:
            honours = self.qualification.label + " "

        english_title = honours + self.english_title
        welsh_title = honours + self.welsh_title

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
        self.name = data_obj.get('name')
        self.code = data_obj.get('code')


class CourseDistanceLearning:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')

    def display_label(self):
        return DICT.get('distance_learning_values').get(self.code).get(self.display_language)


class CourseFoundationYear:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseLength:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseLink:

    def __init__(self, name, link_obj, language_key):
        self.label = name
        if language_key in link_obj:
            self.link = link_obj.get(language_key)
        else:
            self.link = link_obj.get(enums.languages_full.ENGLISH)


class CourseLocation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.latitude = data_obj.get('latitude')
        self.longitude = data_obj.get('longitude')
        name = data_obj.get('name')
        if name:
            self.english_name = name.get('english')
            self.welsh_name = name.get('welsh')
        self.links = data_obj.get('links')

    def display_name(self):
        return self.english_name if self.display_language == enums.languages.ENGLISH else self.welsh_name


class CourseMode:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseQualification:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseSandwichYear:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseYearAbroad:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class EntryStatistics:

    def __init__(self, data_obj):
        self.a_level = data_obj.get('a-level')
        self.access = data_obj.get('access')
        self.aggregation_level = data_obj.get('aggregation_level')
        self.another_higher_education_qualifications = data_obj.get('another_higher_education_qualifications')
        self.baccalaureate = data_obj.get('baccalaureate')
        self.degree = data_obj.get('degree')
        self.foundation = data_obj.get('foundation')
        self.none = data_obj.get('none')
        self.number_of_students = data_obj.get('number_of_students')
        self.other_qualifications = data_obj.get('other_qualifications')
        self.other_qualifications = data_obj.get('other_qualifications')
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')


class ContinuationStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.dormant = data_obj.get('dormant')
        self.continuing = data_obj.get('continuing_with_provider') if data_obj.get('continuing_with_provider') else 0
        self.gained = data_obj.get('gained') if data_obj.get('gained') else 0
        self.left = data_obj.get('left')
        self.lower = data_obj.get('lower')
        self.number_of_students = data_obj.get('number_of_students')
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')

    @property
    def continuing_or_complete(self):
        return self.continuing + self.gained


class EmploymentStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.unemployed = data_obj.get('assumed_to_be_unemployed')
        self.in_study = data_obj.get('in_study')
        self.in_work = data_obj.get('in_work')
        self.in_work_and_study = data_obj.get('in_work_and_study') if data_obj.get('in_work_and_study') else 0
        self.in_work_or_study = data_obj.get('in_work_or_study') if data_obj.get('in_work_or_study') else 0
        self.not_available_for_work_or_study = data_obj.get('not_available_for_work_or_study')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = str(data_obj.get('response_rate')) + '%'
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')

    @property
    def work_and_or_study(self):
        return self.in_work_or_study


class JobTypeStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.non_professional_or_managerial_jobs = data_obj.get('non_professional_or_managerial_jobs')
        self.professional_or_managerial_jobs = data_obj.get('professional_or_managerial_jobs')
        self.unknown_professions = data_obj.get('unknown_professions')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = str(data_obj.get('response_rate')) + '%'
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')


class SalaryStatistics:

    def __init__(self, data_obj, language, course_title):
        self.display_language = language
        self.aggregation_level = data_obj.get('aggregation_level')
        self.higher_quartile = data_obj.get('higher_quartile')
        self.lower_quartile = data_obj.get('lower_quartile')
        self.median = data_obj.get('median')
        self.sector_higher_quartile = data_obj.get('sector_higher_quartile')
        self.sector_lower_quartile = data_obj.get('sector_lower_quartile')
        self.sector_median = data_obj.get('sector_median')
        self.number_of_students = data_obj.get('number_of_graduates')
        self.response_rate = str(data_obj.get('response_rate')) + '%'
        subject = data_obj.get('subject')
        if subject:
            self.subject_code = subject.get('code')
            self.subject_english_label = subject.get("english_label")
            self.subject_welsh_label = subject.get("welsh_label")
        elif course_title:
            self.subject_english_label = course_title.get("english")
            self.subject_welsh_label = course_title.get("welsh")
        else:
            self.subject_english_label = ''
            self.subject_welsh_label = ''
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')

    def display_subject_label(self):
        return self.subject_english_label if self.display_language == enums.languages.ENGLISH else\
            self.subject_welsh_label


class LEOStatistics:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.aggregation_level = data_obj.get("aggregation_level")
        self.higher_quartile = data_obj.get("higher_quartile")
        self.lower_quartile = data_obj.get("lower_quartile")
        self.median = data_obj.get("median")
        self.number_of_graduates = data_obj.get("number_of_graduates")
        subject = data_obj.get('subject')
        if subject:
            self.subject_code = subject.get('code')
            self.subject_english_label = subject.get("english_label")
            self.subject_welsh_label = subject.get("welsh_label")
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')

    def display_subject_label(self):
        return self.subject_english_label if self.display_language == enums.languages.ENGLISH else\
            self.subject_welsh_label


class SatisfactionStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = str(data_obj.get('response_rate')) + '%'
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
            self.unavailable_reason = unavailable_data.get('reason')


class SatisfactionQuestion:

    def __init__(self, question_data):
        if question_data:
            self.description = question_data.get('description')
            self.agree_or_strongly_agree = question_data.get('agree_or_strongly_agree')


class TariffStatistics:

    def __init__(self, tariff_data):
        self.aggregation = tariff_data.get('aggregation')
        self.number_of_students = tariff_data.get('number_of_students')
        self.tariffs = []
        if tariff_data.get('tariffs'):
            for tariff in tariff_data.get('tariffs'):
                self.tariffs.append(Tariff(tariff))
        self.tariffs.reverse()


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
        self.description = tariff.get('description')
        self.entrants = tariff.get('entrants')

    @property
    def label(self):
        return self.LABELS[self.code]


class CourseAccreditation:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.type = data_obj.get("type")
        self.accreditor_url = data_obj.get('accreditor_url')
        text = data_obj.get('text')
        if text:
            self.text_english = text.get('english')
            self.text_welsh = text.get('welsh')
        url = data_obj.get('url')
        self.url_english = url.get('english') if url else None
        dependent = data_obj.get('dependent_on')
        if dependent:
            self.dependent_on_code = dependent.get('code')
            self.dependent_on_label = dependent.get('label')

    def display_text(self):
        return self.text_english if self.display_language == enums.languages.ENGLISH else self.text_welsh

    def language_url(self):
        return self.url_english if self.url_english else self.accreditor_url
