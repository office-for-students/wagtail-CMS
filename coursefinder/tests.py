from unittest.mock import patch

from CMS.test.mocks import SearchMocks
from CMS.test.utils import UniSimpleTestCase
from coursefinder.models import CourseSearch
from errors.models import ApiError


class CourseFinderModelsTests(UniSimpleTestCase):

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
