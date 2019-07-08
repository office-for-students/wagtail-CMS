from wagtail.core.models import Site

from coursefinder.models import CourseFinderResults, CourseFinderLandingPage, CourseFinderChooseCountry, \
    CourseFinderModeOfStudy


class PageFactory:

    @classmethod
    def create_test_course_finder_results_page(cls, title='Test page', path="1111", depth=0):
        course_finder_results = CourseFinderResults(title=title, path=path, depth=depth).save()
        return course_finder_results

    @classmethod
    def create_course_finder_landing_page(cls, title='Test page', path="1111", depth=0):
        site = Site.objects.first()
        if not site.site_name:
            site.site_name = 'unisimpletest'
            site.save()

        root_page = site.root_page
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
