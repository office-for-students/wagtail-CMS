from wagtail.core.models import Site

from coursefinder.models import CourseFinderResults, CourseFinderLandingPage, CourseFinderChooseCountry, \
    CourseFinderModeOfStudy, CourseFinderChooseSubject, CourseFinderNarrowSearch, CourseFinderPostcode, \
    CourseFinderSummary, CourseFinderUni
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
    def create_course_finder_landing_page(cls, title='Test page', path="1111", depth=0):
        root_page = cls.get_root_page()
        course_finder_landing = CourseFinderLandingPage(title=title, path=path, depth=depth, live=True)
        root_page.add_child(instance=course_finder_landing)

        course_finder_landing.save_revision().publish()
        course_finder_landing.save()

        return course_finder_landing

    @classmethod
    def create_country_finder_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        country_finder_page = CourseFinderChooseCountry(title=title, path=path, depth=depth)

        parent_page.add_child(instance=country_finder_page)

        country_finder_page.save_revision().publish()
        country_finder_page.save()

        return country_finder_page

    @classmethod
    def create_mode_of_study_finder_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        mode_of_study_finder_page = CourseFinderModeOfStudy(title=title, path=path, depth=depth)

        parent_page.add_child(instance=mode_of_study_finder_page)

        mode_of_study_finder_page.save_revision().publish()
        mode_of_study_finder_page.save()

        return mode_of_study_finder_page

    @classmethod
    def create_choose_subject_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        choose_subject_page = CourseFinderChooseSubject(title=title, path=path, depth=depth)

        parent_page.add_child(instance=choose_subject_page)

        choose_subject_page.save_revision().publish()
        choose_subject_page.save()

        return choose_subject_page

    @classmethod
    def create_narrow_search_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        narrow_search_page = CourseFinderNarrowSearch(title=title, path=path, depth=depth)

        parent_page.add_child(instance=narrow_search_page)

        narrow_search_page.save_revision().publish()
        narrow_search_page.save()

        return narrow_search_page

    @classmethod
    def create_uni_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        uni_page = CourseFinderUni(title=title, path=path, depth=depth)

        parent_page.add_child(instance=uni_page)

        uni_page.save_revision().publish()
        uni_page.save()

        return uni_page

    @classmethod
    def create_postcode_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        postcode_page = CourseFinderPostcode(title=title, path=path, depth=depth)

        parent_page.add_child(instance=postcode_page)

        postcode_page.save_revision().publish()
        postcode_page.save()

        return postcode_page

    @classmethod
    def create_summary_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        summary_page = CourseFinderSummary(title=title, path=path, depth=depth)

        parent_page.add_child(instance=summary_page)

        summary_page.save_revision().publish()
        summary_page.save()

        return summary_page

    @classmethod
    def create_results_page(cls, title='Test page', path="11111111", depth=1, parent_page=None):
        if not parent_page:
            parent_page = cls.create_course_finder_landing_page('Course Finder')
        results_page = CourseFinderResults(title=title, path=path, depth=depth)

        parent_page.add_child(instance=results_page)

        results_page.save_revision().publish()
        results_page.save()

        return results_page

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
