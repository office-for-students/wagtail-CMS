import statistics

from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core import blocks

from courses import request_handler
from errors.models import ApiError
from institutions.models import Institution

DATA_SET_KEYS = (
    ('student_satisfaction', 'Student satisfaction'),
    ('entry_information', 'Entry information'),
    ('after_one_year', 'After 1 year of study'),
    ('after_the_course', 'After the course'),
    ('professional_accreditation', 'Professional accreditation'),
)


class AccordionPanel(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    data_set = blocks.ChoiceBlock(choices=DATA_SET_KEYS,
                                  default='standard')


class CourseDetailPage(Page):
    accordions = StreamField([
        ('accordion_panel', AccordionPanel(required=True, icon='collapse-down'))
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

    def __init__(self, data_obj):
        self.id = data_obj.get('id')
        course_details = data_obj.get('course')
        if course_details:
            self.country = CourseCountry(course_details.get('country'))
            self.distance_learning = CourseDistanceLearning(course_details.get('distance_learning'))
            self.foundation_year = CourseFoundationYear(course_details.get('foundation_year_availability'))
            self.honours_award_provision = course_details.get('honours_award_provision')
            self.institution = Institution(course_details.get('institution'))
            self.kis_course_id = course_details.get('kis_course_id')
            self.length = CourseLength(course_details.get('length_of_course'))
            self.course_links = []
            for name, link in course_details.get('links').items():
                if type(link) != list:
                    self.course_links.append(CourseLink(name, link))
            self.locations = []
            for location in course_details.get('locations'):
                self.locations.append(CourseLocation(location))
            self.mode = CourseMode(course_details.get('mode'))
            self.qualification = CourseQualification(course_details.get('qualification'))
            self.sandwich_year = CourseSandwichYear(course_details.get('sandwich_year'))
            self.english_title = course_details.get('title').get('english')
            self.welsh_title = course_details.get('title').get('welsh')
            self.ucas_programme_id = course_details.get('ucas_programme_id')
            self.year_abroad = CourseYearAbroad(course_details.get('year_abroad'))
            stats = course_details.get('statistics')
            self.entry_stats = EntryStatistics(stats.get('entry')[0])
            self.continuation_stats = ContinuationStatistics(stats.get('continuation')[0])
            self.employment_stats = EmploymentStatistics(stats.get('employment')[0])
            self.job_type_stats = JobTypeStatistics(stats.get('job_type')[0])
            self.salary_stats = SalaryStatistics(stats.get('salary')[0])
            self.satisfaction_stats = SatisfactionStatistics(stats.get('nss')[0])

    @property
    def number_of_locations(self):
        return len(self.locations)

    @property
    def locations_list(self):
        location_names = []
        for location in self.locations:
            location_names.append(location.english_name)
        return ', '.join(location_names)

    @classmethod
    def find(cls, institution_id, course_id, mode):
        course = None
        error = None

        response = request_handler.load_course_data(institution_id, course_id, cls.get_mode_code(mode))

        if response.ok:
            course = cls(response.json())
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

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseFoundationYear:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseLength:

    def __init__(self, data_obj):
        self.code = data_obj.get('code')
        self.label = data_obj.get('label')


class CourseLink:

    def __init__(self, name, link_obj):
        self.label = name.replace('_', ' ').capitalize()
        self.link = link_obj.get('english')


class CourseLocation:

    def __init__(self, data_obj):
        self.latitude = data_obj.get('latitude')
        self.longitude = data_obj.get('longitude')
        self.english_name = data_obj.get('name').get('english')
        self.welsh_name = data_obj.get('name').get('welsh')


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
        self.continuing = data_obj.get('continuing_with_provider')
        self.dormant = data_obj.get('dormant')
        self.gained = data_obj.get('gained')
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
        self.in_work_and_study = data_obj.get('in_work_and_study')
        self.in_work_or_study = data_obj.get('in_work_or_study')
        self.not_available_for_work_or_study = data_obj.get('not_available_for_work_or_study')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = data_obj.get('response_rate')
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')

    @property
    def work_and_or_study(self):
        return self.in_work_and_study + self.in_work_or_study


class JobTypeStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.non_professional_or_managerial_jobs = data_obj.get('non_professional_or_managerial_jobs')
        self.professional_or_managerial_jobs = data_obj.get('professional_or_managerial_jobs')
        self.unknown_professions = data_obj.get('unknown_professions')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = data_obj.get('resp_rate')
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')


class SalaryStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.higher_quartile = data_obj.get('higher_quartile')
        self.lower_quartile = data_obj.get('lower_quartile')
        self.number_of_students = data_obj.get('number_of_graduates')
        self.response_rate = data_obj.get('response_rate')
        unavailable_data = data_obj.get('unavailable')
        if unavailable_data:
            self.unavailable_code = unavailable_data.get('code')
            self.unavailable_reason = unavailable_data.get('reason')

    @property
    def mean(self):
        return round(statistics.mean([self.higher_quartile, self.lower_quartile]))


class SatisfactionStatistics:

    def __init__(self, data_obj):
        self.aggregation_level = data_obj.get('aggregation_level')
        self.number_of_students = data_obj.get('number_of_students')
        self.response_rate = data_obj.get('resp_rate')
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


class SatisfactionQuestion:

    def __init__(self, question_data):
        self.description = question_data.get('description')
        self.agree_or_strongly_agree = question_data.get('agree_or_strongly_agree')
