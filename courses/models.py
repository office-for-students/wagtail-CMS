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
            self.course_links = course_details.get('links')
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

        response = request_handler.load_course_data(institution_id, course_id, mode)

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

