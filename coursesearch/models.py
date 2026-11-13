import math

from django.db.models.fields import TextField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import PageChooserBlock
from wagtail.fields import RichTextField
from wagtail.fields import StreamField

from CMS.enums import enums
from core.models import DiscoverUniBasePage
from core.utils import get_page_for_language

from coursesearch.utils import choose_country_sibling_finder
from coursesearch.utils import choose_subject_sibling_finder
from coursesearch.utils import mode_of_study_sibling_finder
from coursesearch.utils import narrow_search_sibling_finder
from coursesearch.utils import results_sibling_finder
from coursesearch.utils import summary_sibling_finder
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
        ('links', PageChooserBlock()),
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('related_links_title'),
        FieldPanel('related_links', classname="full"),
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

