from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from django.db.models.fields import TextField

from core.models import DiscoverUniBasePage
from core.utils import get_page_for_language
from coursefinder.models import CourseFinderChooseCountry


class SearchLandingPage(DiscoverUniBasePage):

    heading = TextField(blank=False)
    search_heading = TextField(blank=False)
    course_finder_heading = TextField(blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('heading', classname="full"),
        FieldPanel('search_heading', classname="full"),
        FieldPanel('course_finder_heading', classname="full"),
    ]

    def get_context(self, request):
        context = super(SearchLandingPage, self).get_context(request)
        context['search_url'] = '/search-results'
        context['course_finder_url'] = get_page_for_language(self.get_language(),
                                                             CourseFinderChooseCountry.objects.all()).url
        return context
