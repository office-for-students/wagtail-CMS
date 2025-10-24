from django.db.models.fields import TextField
from wagtail.admin.panels import FieldPanel

from CMS.enums import enums
from core.models import DiscoverUniBasePage
from core.utils import get_page_for_language
from coursefinder.models import CourseFinderChooseCountry
from institutions.models import InstitutionList


class SearchLandingPage(DiscoverUniBasePage):
    heading = TextField(blank=False)
    search_heading = TextField(blank=False)
    search_button_description = TextField(blank=False)
    course_finder_heading = TextField(blank=False)
    course_finder_button_description = TextField(blank=False)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('search_heading', classname="full"),
        FieldPanel('search_button_description', classname="full"),
        FieldPanel('course_finder_heading', classname="full"),
        FieldPanel('course_finder_button_description', classname="full"),
    ]

    def get_context(self, request):
        context = super(SearchLandingPage, self).get_context(request)
        context['search_url'] = self.get_search_url()
        context['course_finder_url'] = get_page_for_language(self.get_language(),
                                                             CourseFinderChooseCountry.objects.all()).url
        context['institutions_list'] = InstitutionList.get_options()[self.get_language()]

        return context

    def get_search_url(self):
        if self.get_language() == enums.languages.WELSH:
            return "/%s/course-finder/results/" % self.get_language()
        return '/course-finder/results/'
