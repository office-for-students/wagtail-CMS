from wagtail.models import Site

from coursesearch.models import (
    CourseFinderResults,
    CourseFinderChooseCountry,
    CourseFinderModeOfStudy,
    CourseFinderChooseSubject,
    CourseFinderNarrowSearch,
    CourseFinderPostcode,
    CourseFinderSummary,
    CourseFinderUni
)
from home.models import HomePage

class PageFactory:

    @classmethod
    def create_home_page(cls, title='Test home page', path='1', depth=0):
        root_page = cls.get_root_page()
        home_page = HomePage(title=title, path=path, depth=depth)
        root_page.add_child(instance=home_page)
        home_page.save()
        return home_page

    @classmethod
    def create_test_course_finder_results_page(cls, title='Test page', path="1111", depth=0):
        root_page = cls.get_root_page()
        course_finder_results = CourseFinderResults(title=title, path=path, depth=depth)
        root_page.add_child(instance=course_finder_results)
        course_finder_results.save()
        return course_finder_results

    @classmethod
    def get_root_page(cls):
        return cls.get_site().root_page

    @classmethod
    def get_site(cls):
        site = Site.objects.first()
        if not site.site_name:
            site.site_name = 'unisimpletest'
            site.save()
        return site
