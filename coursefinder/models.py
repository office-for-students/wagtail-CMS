import math

from django.db.models.fields import TextField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from CMS.enums import enums
from core.models import DiscoverUniBasePage
from core.utils import get_page_for_language
from coursefinder import request_handler
from coursefinder.utils import choose_country_sibling_finder, mode_of_study_sibling_finder, \
    choose_subject_sibling_finder, narrow_search_sibling_finder, summary_sibling_finder, \
    results_sibling_finder
from errors.models import ApiError
from institutions.models import InstitutionList


class CourseFinderChooseCountry(DiscoverUniBasePage):
    page_order = 1
    question = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('question', classname="full"),
    ]

    @property
    def next_page(self):
        return mode_of_study_sibling_finder(self)

    @property
    def back_page(self):
        from site_search.models import SearchLandingPage
        return get_page_for_language(self.get_language(), SearchLandingPage.objects.all())


class CourseFinderModeOfStudy(DiscoverUniBasePage):
    page_order = 2
    question = TextField(blank=True)
    helper_text = RichTextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('question', classname="full"),
        FieldPanel('helper_text', classname="full")
    ]

    @property
    def next_page(self):
        return choose_subject_sibling_finder(self)

    @property
    def back_page(self):
        return choose_country_sibling_finder(self.get_siblings().specific())


class CourseFinderChooseSubject(DiscoverUniBasePage):
    page_order = 3
    question = TextField(blank=True)
    helper_text = RichTextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('question', classname="full"),
        FieldPanel('helper_text', classname="full")
    ]

    @property
    def next_page(self):
        return narrow_search_sibling_finder(self)

    @property
    def back_page(self):
        return mode_of_study_sibling_finder(self)


class CourseFinderNarrowSearch(DiscoverUniBasePage):
    page_order = 4
    use_skip_form = True
    question = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('question', classname="full")
    ]

    @property
    def back_page(self):
        return choose_subject_sibling_finder(self)


class CourseFinderUni(DiscoverUniBasePage):
    page_order = 6
    use_skip_form = True
    question = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('question', classname="full")
    ]

    @property
    def next_page(self):
        return summary_sibling_finder(self)

    @property
    def back_page(self):
        return narrow_search_sibling_finder(self)

    def get_context(self, request):
        context = super().get_context(request)
        context['institutions_list'] = InstitutionList.get_options()[self.get_language()]
        return context


class CourseFinderPostcode(DiscoverUniBasePage):
    page_order = 7
    use_skip_form = True
    question = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('question', classname="full")
    ]

    @property
    def next_page(self):
        return summary_sibling_finder(self)

    @property
    def back_page(self):
        return narrow_search_sibling_finder(self)


class CourseFinderSummary(DiscoverUniBasePage):
    page_order = 8
    header = TextField(blank=True)
    country_section_title = TextField(blank=True)
    mode_of_study_section_title = TextField(blank=True)
    subjects_section_title = TextField(blank=True)
    narrow_by_section_title = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('country_section_title', classname="full"),
        FieldPanel('mode_of_study_section_title', classname="full"),
        FieldPanel('subjects_section_title', classname="full"),
        FieldPanel('narrow_by_section_title', classname="full")
    ]

    @property
    def next_page(self):
        return results_sibling_finder(self)

    @property
    def back_page(self):
        return narrow_search_sibling_finder(self)


class CourseFinderResults(DiscoverUniBasePage):
    page_order = 9
    header = TextField(blank=True)
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock()),
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('related_links_title'),
        StreamFieldPanel('related_links', classname="full"),
    ]
    
    def get_context(self, request):
        context = super(CourseFinderResults, self).get_context(request)
        context['search_url'] = self.get_search_url()
        context['course_finder_url'] = get_page_for_language(self.get_language(),
                                                             CourseFinderChooseCountry.objects.all()).url
        context['institutions_list'] = InstitutionList.get_options()[self.get_language()]

        return context

    def get_search_url(self):
        if self.get_language() == enums.languages.WELSH:
            return "/%s/course-finder/results/" % self.get_language()
        return '/course-finder/results/'


class BaseSearch:

    def __init__(self, page, count):
        self.page = int(page) if page else 1
        self.count = int(count) if page else 20
        self.offset = self.count * (self.page - 1)
        self.total_courses = None
        self.total_institutions = None
        self.results = None

    @property
    def show_previous_icon(self):
        return bool(self.pages_to_left)

    @property
    def previous_page(self):
        return self.page - 1

    @property
    def show_ellipsis_on_left(self):
        return self.previous_page > 1

    @property
    def pages_to_left(self):
        if self.page == 1 or self.total_page_count == 0:
            return []
        if self.page == self.total_page_count and self.total_page_count != 2:
            return [self.page - 2, self.previous_page]
        return [self.previous_page]

    @property
    def pages_to_right(self):
        if self.page == self.total_page_count or self.total_page_count == 0:
            return []
        if self.page == 1 and self.total_page_count != 2:
            return [self.next_page, self.page + 2]
        return [self.next_page]

    @property
    def show_ellipsis_on_right(self):
        return self.pages_to_right and self.pages_to_right[-1] != self.total_page_count

    @property
    def next_page(self):
        return self.page + 1

    @property
    def show_next_icon(self):
        return bool(self.pages_to_right)

    @property
    def total_page_count(self):
        return math.ceil(self.total_institutions / self.count)


class CourseSearch(BaseSearch):

    def __init__(self, subject, institution, page, count, language=enums.languages.ENGLISH):
        super().__init__(page, count)
        self.subject = subject
        self.institution = institution
        self.total_courses = None
        self.total_institutions = None
        self.results = None
        self.language = language

    def execute(self):
        response = request_handler.query_course_and_institution(self.subject, self.institution, self.count, self.offset, self.language)
        error = None

        if response.ok:
            data = response.json()
            self.total_courses = data.get('total_number_of_courses')
            self.total_institutions = data.get('total_results')
            self.results = data.get('items')
        else:
            error = ApiError(response.status_code, 'searching courses for %s %s' %
                             (self.institution, self.subject))

        return error


class CourseFinderSearch(BaseSearch):

    def __init__(self, subject, institution, countries, postcode, filters, course, page, count, language=enums.languages.ENGLISH):
        super().__init__(page, count)
        self.subject = subject
        self.institution = institution
        self.countries = countries
        self.postcode = postcode
        self.filters = filters
        self.course = course
        self.language = language

    def execute(self):
        response = request_handler.course_finder_query(self.subject, self.institution, self.countries, self.postcode,
                                                       self.filters, self.course, self.count, self.offset, self.language)
        error = None

        if response.ok:
            data = response.json()
            self.total_courses = data.get('total_number_of_courses')
            self.total_institutions = data.get('total_results')
            self.results = data.get('items')
        else:
            error = ApiError(response.status_code, 'searching courses for %s, %s, %s' %
                             (self.subject, self.institution, self.countries))

        return error
