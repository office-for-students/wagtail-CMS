from unittest.mock import patch

from CMS.test.factories import PageFactory
from CMS.test.mocks import SearchMocks
from CMS.test.utils import UniSimpleTestCase
from coursefinder.models import CourseSearch
from errors.models import ApiError


class CourseFinderModelsTests(UniSimpleTestCase):

    def test_course_finder_landing_page_country_finder_page_returns_child_if_country_finder_child_exists(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        PageFactory.create_country_finder_page(title='Country Finder', parent_page=course_finder_page)
        self.assertIsNotNone(course_finder_page.country_finder_page)

    def test_course_finder_landing_page_country_finder_page_returns_first_child_if_multiple_country_finder_child_exists(
            self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        country_finder_1 = PageFactory.create_country_finder_page(title='Country Finder',
                                                                  parent_page=course_finder_page)
        country_finder_2 = PageFactory.create_country_finder_page(title='Country Finder 2', path='11111112',
                                                                  parent_page=course_finder_page)
        self.assertIsNotNone(course_finder_page.country_finder_page)
        self.assertNotEquals(country_finder_1.title, country_finder_2.title)
        self.assertEquals(course_finder_page.country_finder_page.title, country_finder_1.title)

    def test_course_finder_landing_page_country_finder_page_returns_country_finder_child_if_multiple_child_types_exists(
            self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        country_finder = PageFactory.create_country_finder_page(title='Country Finder',
                                                                parent_page=course_finder_page)
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=course_finder_page)
        self.assertIsNotNone(course_finder_page.country_finder_page)
        self.assertNotEquals(country_finder.title, mode_of_study_finder.title)
        self.assertEquals(course_finder_page.country_finder_page.title, country_finder.title)

    def test_course_finder_landing_page_country_finder_page_returns_none_if_no_country_finder_child_exists(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        self.assertIsNone(course_finder_page.country_finder_page)

    def test_course_finder_landing_page_has_country_finder_page_returns_true_if_country_finder_child_exists(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        PageFactory.create_country_finder_page(title='Country Finder', parent_page=course_finder_page)
        self.assertIsTrue(course_finder_page.has_country_finder_page())

    def test_course_finder_landing_page_has_country_finder_page_returns_false_if_no_country_finder_child_exists(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        self.assertIsFalse(course_finder_page.has_country_finder_page())

    def test_course_finder_results_execute_function_appends_counts_and_list_of_courses_to_model_on_success(self):
        mock_data = SearchMocks.get_search_response_content()
        course_search = CourseSearch("", "")
        error = course_search.execute()
        self.assertIsNone(error)
        self.assertEquals(course_search.total_courses, mock_data.get('total_number_of_courses'))
        self.assertEquals(course_search.total_institutions, mock_data.get('total_results'))
        self.assertEquals(type(course_search.results), list)
        self.assertEquals(len(course_search.results), len(mock_data.get('items')))

    @patch('coursefinder.request_handler.query_course_and_institution',
           return_value=SearchMocks.get_unsuccessful_search_response())
    def test_course_finder_results_execute_function_returns_error_on_failure(self, mock_search):
        course_search = CourseSearch("", "")
        error = course_search.execute()
        self.assertIsNone(course_search.total_courses)
        self.assertIsNone(course_search.total_institutions)
        self.assertIsNone(course_search.results)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), ApiError)
