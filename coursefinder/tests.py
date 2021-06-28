from django.test import tag
from unittest.mock import patch

from CMS.test.factories import PageFactory
from CMS.test.mocks.search_mocks import SearchMocks
from CMS.test.utils import UniSimpleTestCase
from coursefinder.models import CourseSearch, CourseFinderChooseCountry, CourseFinderModeOfStudy, \
    CourseFinderChooseSubject, CourseFinderNarrowSearch, CourseFinderPostcode, CourseFinderSummary, \
    CourseFinderResults, CourseFinderSearch, BaseSearch
from coursefinder.utils import choose_country_sibling_finder, mode_of_study_sibling_finder, \
    choose_subject_sibling_finder, narrow_search_sibling_finder, postcode_sibling_finder, summary_sibling_finder, \
    results_sibling_finder
from coursefinder.views import build_study_mode_filter
from errors.models import ApiError
from site_search.models import SearchLandingPage


@tag('azure')
class CourseFinderModelsTests(UniSimpleTestCase):

    def test_course_search_execute_function_appends_counts_and_list_of_courses_to_model_on_success(self):
        mock_data = SearchMocks.get_search_response_content()
        course_search = CourseSearch("Computing", None, 1, 20)
        error = course_search.execute()
        self.assertIsNone(error)
        self.assertEquals(course_search.total_courses, mock_data.get('total_number_of_courses'))
        self.assertEquals(course_search.total_institutions, mock_data.get('total_results'))
        self.assertEquals(type(course_search.results), list)
        self.assertEquals(len(course_search.results), len(mock_data.get('items')))

    @patch('coursefinder.request_handler.query_course_and_institution',
           return_value=SearchMocks.get_unsuccessful_search_response())
    def test_course_search_execute_function_returns_error_on_failure(self, mock_search):
        course_search = CourseSearch("Computing", None, 1, 20)
        error = course_search.execute()
        self.assertIsNone(course_search.total_courses)
        self.assertIsNone(course_search.total_institutions)
        self.assertIsNone(course_search.results)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), ApiError)

    def test_course_finder_choose_country_next_page_returns_mode_of_study_sibling(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder', path='11111112',
                                                     parent_page=country_finder.get_parent())

        self.assertIsNotNone(country_finder.next_page)
        self.assertEquals(type(country_finder.next_page), CourseFinderModeOfStudy)

    def test_course_finder_choose_country_back_page_returns_parent_page(self):
        course_finder_page = PageFactory.create_search_landing_page('Course Finder')
        country_finder = PageFactory.create_country_finder_page(title='Country Finder', parent_page=course_finder_page)

        self.assertIsNotNone(country_finder.back_page)
        self.assertEquals(type(country_finder.back_page), SearchLandingPage)

    def test_course_finder_mode_of_study_next_page_returns_choose_subject_sibling(self):
        mode_of_study = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder')
        PageFactory.create_choose_subject_page(title='Subject Chooser', path='11111112',
                                               parent_page=mode_of_study.get_parent())

        self.assertIsNotNone(mode_of_study.next_page)
        self.assertEquals(type(mode_of_study.next_page), CourseFinderChooseSubject)

    def test_course_finder_mode_of_study_back_page_returns_choose_country_sibling(self):
        mode_of_study = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder')
        PageFactory.create_country_finder_page(title='Country Finder', parent_page=mode_of_study.get_parent())

        self.assertIsNotNone(mode_of_study.back_page)
        self.assertEquals(type(mode_of_study.back_page), CourseFinderChooseCountry)

    def test_course_finder_choose_subject_next_page_returns_narrow_search_sibling(self):
        choose_subject = PageFactory.create_choose_subject_page(title='Subject Chooser')
        PageFactory.create_narrow_search_page(title='Narrow Search', path='11111112',
                                              parent_page=choose_subject.get_parent())

        self.assertIsNotNone(choose_subject.next_page)
        self.assertEquals(type(choose_subject.next_page), CourseFinderNarrowSearch)

    def test_course_finder_choose_subject_back_page_returns_mode_of_study_sibling(self):
        choose_subject = PageFactory.create_choose_subject_page(title='Subject Chooser')
        PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder', path='11111112',
                                                     parent_page=choose_subject.get_parent())

        self.assertIsNotNone(choose_subject.back_page)
        self.assertEquals(type(choose_subject.back_page), CourseFinderModeOfStudy)

    def test_course_finder_narrow_search_back_page_returns_choose_subject_sibling(self):
        narrow_search = PageFactory.create_narrow_search_page(title='Narrow Search')
        PageFactory.create_choose_subject_page(title='Subject Chooser', path='11111112',
                                               parent_page=narrow_search.get_parent())

        self.assertIsNotNone(narrow_search.back_page)
        self.assertEquals(type(narrow_search.back_page), CourseFinderChooseSubject)

    def test_course_finder_uni_next_page_returns_summary_sibling(self):
        uni = PageFactory.create_uni_page(title='Uni')
        PageFactory.create_summary_page(title='Summary', path='11111112', parent_page=uni.get_parent())

        self.assertIsNotNone(uni.next_page)
        self.assertEquals(type(uni.next_page), CourseFinderSummary)

    def test_course_finder_uni_back_page_returns_narrow_search_sibling(self):
        uni = PageFactory.create_uni_page(title='Uni')
        PageFactory.create_narrow_search_page(title='Narrow Search', path='11111112', parent_page=uni.get_parent())

        self.assertIsNotNone(uni.back_page)
        self.assertEquals(type(uni.back_page), CourseFinderNarrowSearch)

    def test_course_finder_postcode_next_page_returns_summary_sibling(self):
        postcode = PageFactory.create_postcode_page(title='Postcode')
        PageFactory.create_summary_page(title='Summary', path='11111112', parent_page=postcode.get_parent())

        self.assertIsNotNone(postcode.next_page)
        self.assertEquals(type(postcode.next_page), CourseFinderSummary)

    def test_course_finder_postcode_back_page_returns_narrow_search_sibling(self):
        postcode = PageFactory.create_postcode_page(title='Postcode')
        PageFactory.create_narrow_search_page(title='Narrow Search', path='11111112', parent_page=postcode.get_parent())

        self.assertIsNotNone(postcode.back_page)
        self.assertEquals(type(postcode.back_page), CourseFinderNarrowSearch)

    def test_course_finder_summary_next_page_returns_results_sibling(self):
        summary = PageFactory.create_summary_page(title='Summary')
        PageFactory.create_results_page(title='Results', path='11111112', parent_page=summary.get_parent())

        self.assertIsNotNone(summary.next_page)
        self.assertEquals(type(summary.next_page), CourseFinderResults)

    def test_course_finder_summary_back_page_returns_narrow_search_sibling(self):
        summary = PageFactory.create_summary_page(title='Summary')
        PageFactory.create_narrow_search_page(title='Postcode', path='11111112', parent_page=summary.get_parent())

        self.assertIsNotNone(summary.back_page)
        self.assertEquals(type(summary.back_page), CourseFinderNarrowSearch)

    def test_course_finder_search_execute_function_appends_counts_and_list_of_courses_to_model_on_success(self):
        mock_data = SearchMocks.get_search_response_content()
        course_finder_search = CourseFinderSearch("Computing", None, None, None, None, None, None, None, 1, 20)
        error = course_finder_search.execute()
        self.assertIsNone(error)
        self.assertEquals(course_finder_search.total_courses, mock_data.get('total_number_of_courses'))
        self.assertEquals(course_finder_search.total_institutions, mock_data.get('total_results'))
        self.assertEquals(type(course_finder_search.results), list)
        self.assertEquals(len(course_finder_search.results), len(mock_data.get('items')))

    @patch('coursefinder.request_handler.course_finder_query',
           return_value=SearchMocks.get_unsuccessful_search_response())
    def test_course_finder_search_execute_function_returns_error_on_failure(self, mock_search):
        course_finder_search = CourseFinderSearch("Computing", None, None, None, None, None, None, None, 1, 20)
        error = course_finder_search.execute()
        self.assertIsNone(course_finder_search.total_courses)
        self.assertIsNone(course_finder_search.total_institutions)
        self.assertIsNone(course_finder_search.results)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), ApiError)

    def test_base_search_total_page_count_correctly_calculates(self):
        base_search = BaseSearch(1, 20)
        base_search.total_institutions = 77
        actual = base_search.total_page_count

        expected = 4
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_left_returns_empty_list_on_page_one(self):
        base_search = BaseSearch(1, 20)
        base_search.total_institutions = 77
        actual = base_search.pages_to_left

        expected = []
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_left_returns_two_element_list_on_last_page_when_more_than_two_pages(self):
        base_search = BaseSearch(4, 20)
        base_search.total_institutions = 77
        actual = base_search.pages_to_left

        expected = [2, 3]
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_left_returns_one_element_list_on_last_page_when_only_two_pages(self):
        base_search = BaseSearch(2, 20)
        base_search.total_institutions = 40
        actual = base_search.pages_to_left

        expected = [1]
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_left_returns_one_element_list_on_page_in_middle_of_range(self):
        base_search = BaseSearch(4, 20)
        base_search.total_institutions = 200
        actual = base_search.pages_to_left

        expected = [3]
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_right_returns_empty_list_on__last_page(self):
        base_search = BaseSearch(4, 20)
        base_search.total_institutions = 77
        actual = base_search.pages_to_right

        expected = []
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_right_returns_two_element_list_on_page_one_when_more_than_two_pages(self):
        base_search = BaseSearch(1, 20)
        base_search.total_institutions = 77
        actual = base_search.pages_to_right

        expected = [2, 3]
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_right_returns_one_element_list_on_page_one_when_only_two_pages(self):
        base_search = BaseSearch(1, 20)
        base_search.total_institutions = 40
        actual = base_search.pages_to_right

        expected = [2]
        self.assertEquals(actual, expected)

    def test_base_search_pages_to_right_returns_one_element_list_on_page_in_middle_of_range(self):
        base_search = BaseSearch(4, 20)
        base_search.total_institutions = 200
        actual = base_search.pages_to_right

        expected = [5]
        self.assertEquals(actual, expected)

    def test_base_search_show_previous_icon_returns_true_when_there_are_pages_to_the_left(self):
        base_search = BaseSearch(4, 20)
        base_search.total_institutions = 200
        actual = base_search.show_previous_icon

        self.assertIsTrue(actual)

    def test_base_search_show_previous_icon_returns_true_when_there_are_no_pages_to_the_left(self):
        base_search = BaseSearch(1, 20)
        base_search.total_institutions = 200
        actual = base_search.show_previous_icon

        self.assertIsFalse(actual)

    def test_base_search_show_next_icon_returns_true_when_there_are_pages_to_the_rigth(self):
        base_search = BaseSearch(4, 20)
        base_search.total_institutions = 200
        actual = base_search.show_next_icon

        self.assertIsTrue(actual)

    def test_base_search_show_next_icon_returns_true_when_there_are_no_pages_to_the_rigth(self):
        base_search = BaseSearch(10, 20)
        base_search.total_institutions = 200
        actual = base_search.show_next_icon

        self.assertIsFalse(actual)

@tag('azure')
class CourseFinderUtilsTests(UniSimpleTestCase):
    def test_choose_country_sibling_finder_returns_country_finder_if_in_list(self):
        course_finder_page = PageFactory.create_search_landing_page('Course Finder')
        PageFactory.create_country_finder_page(title='Country Finder', parent_page=course_finder_page)

        output = choose_country_sibling_finder(course_finder_page.get_children().specific())
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseCountry)

    def test_choose_country_sibling_finder_returns_first_entry_if_multiple_country_finders_in_list(self):
        course_finder_page = PageFactory.create_search_landing_page('Course Finder')
        country_finder_1 = PageFactory.create_country_finder_page(title='Country Finder',
                                                                  parent_page=course_finder_page)
        country_finder_2 = PageFactory.create_country_finder_page(title='Country Finder 2', path='11111112',
                                                                  parent_page=course_finder_page)

        output = choose_country_sibling_finder(course_finder_page.get_children().specific())
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseCountry)
        self.assertNotEquals(country_finder_1.title, country_finder_2.title)
        self.assertEquals(output.title, country_finder_1.title)

    def test_choose_country_sibling_finder_returns_country_finder_if_multiple_page_types_exists(self):
        course_finder_page = PageFactory.create_search_landing_page('Course Finder')
        country_finder = PageFactory.create_country_finder_page(title='Country Finder',
                                                                parent_page=course_finder_page)
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=course_finder_page)

        output = choose_country_sibling_finder(course_finder_page.get_children().specific())
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseCountry)
        self.assertNotEquals(country_finder.title, mode_of_study_finder.title)
        self.assertEquals(output.title, country_finder.title)

    def test_choose_country_sibling_finder_returns_none_if_no_country_finder_page_exists(self):
        course_finder_page = PageFactory.create_search_landing_page('Course Finder')
        output = choose_country_sibling_finder(course_finder_page.get_children().specific())
        self.assertIsNone(output)

    def test_mode_of_study_sibling_finder_returns_mode_of_study_if_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder', path='11111112',
                                                     parent_page=country_finder.get_parent())

        output = mode_of_study_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderModeOfStudy)

    def test_mode_of_study_sibling_finder_returns_first_entry_if_multiple_mode_of_study_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder_1 = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                              path='11111112',
                                                                              parent_page=country_finder.get_parent())
        mode_of_study_finder_2 = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder 2',
                                                                              path='11111113',
                                                                              parent_page=country_finder.get_parent())

        output = mode_of_study_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderModeOfStudy)
        self.assertNotEquals(mode_of_study_finder_1.title, mode_of_study_finder_2.title)
        self.assertEquals(output.title, mode_of_study_finder_1.title)

    def test_mode_of_study_sibling_finder_returns_mode_of_study_if_multiple_page_types_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=country_finder.get_parent())
        subject_chooser = PageFactory.create_choose_subject_page(title='Subject Chooser', path='11111113',
                                                                 parent_page=country_finder.get_parent())

        output = mode_of_study_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderModeOfStudy)
        self.assertNotEquals(mode_of_study_finder.title, subject_chooser.title)
        self.assertEquals(output.title, mode_of_study_finder.title)

    def test_mode_of_study_sibling_finder_returns_none_if_no_mode_of_study_page_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        output = mode_of_study_sibling_finder(country_finder)
        self.assertIsNone(output)

    def test_choose_subject_sibling_finder_returns_choose_subject_if_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_choose_subject_page(title='Subject Chooser', path='11111112',
                                               parent_page=country_finder.get_parent())

        output = choose_subject_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseSubject)

    def test_choose_subject_sibling_finder_returns_first_entry_if_multiple_choose_subject_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        subject_chooser_1 = PageFactory.create_choose_subject_page(title='Subject Chooser', path='11111112',
                                                                   parent_page=country_finder.get_parent())
        subject_chooser_2 = PageFactory.create_choose_subject_page(title='Subject Chooser 2', path='11111113',
                                                                   parent_page=country_finder.get_parent())

        output = choose_subject_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseSubject)
        self.assertNotEquals(subject_chooser_1.title, subject_chooser_2.title)
        self.assertEquals(output.title, subject_chooser_1.title)

    def test_choose_subject_sibling_finder_returns_choose_subject_if_multiple_page_types_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=country_finder.get_parent())
        subject_chooser = PageFactory.create_choose_subject_page(title='Subject Chooser', path='11111113',
                                                                 parent_page=country_finder.get_parent())

        output = choose_subject_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseSubject)
        self.assertNotEquals(mode_of_study_finder.title, subject_chooser.title)
        self.assertEquals(output.title, subject_chooser.title)

    def test_choose_subject_sibling_finder_returns_none_if_no_choose_subject_page_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        output = choose_subject_sibling_finder(country_finder)
        self.assertIsNone(output)

    def test_narrow_search_sibling_finder_returns_narrow_search_if_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_narrow_search_page(title='Narrow Search', path='11111112',
                                              parent_page=country_finder.get_parent())

        output = narrow_search_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderNarrowSearch)

    def test_narrow_search_sibling_finder_returns_first_entry_if_multiple_narrow_search_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        narrow_search_1 = PageFactory.create_narrow_search_page(title='Narrow Search', path='11111112',
                                                                parent_page=country_finder.get_parent())
        narrow_search_2 = PageFactory.create_narrow_search_page(title='Narrow Search 2', path='11111113',
                                                                parent_page=country_finder.get_parent())

        output = narrow_search_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderNarrowSearch)
        self.assertNotEquals(narrow_search_1.title, narrow_search_2.title)
        self.assertEquals(output.title, narrow_search_1.title)

    def test_narrow_search_sibling_finder_returns_narrow_search_if_multiple_page_types_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=country_finder.get_parent())
        narrow_search = PageFactory.create_narrow_search_page(title='Narrow Search', path='11111113',
                                                              parent_page=country_finder.get_parent())

        output = narrow_search_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderNarrowSearch)
        self.assertNotEquals(mode_of_study_finder.title, narrow_search.title)
        self.assertEquals(output.title, narrow_search.title)

    def test_narrow_search_sibling_finder_returns_none_if_no_narrow_search_page_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        output = narrow_search_sibling_finder(country_finder)
        self.assertIsNone(output)

    def test_postcode_sibling_finder_returns_postcode_if_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_postcode_page(title='Postcode', path='11111112',
                                         parent_page=country_finder.get_parent())

        output = postcode_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderPostcode)

    def test_postcode_sibling_finder_returns_first_entry_if_multiple_postcode_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        postcode_1 = PageFactory.create_postcode_page(title='Postcode', path='11111112',
                                                      parent_page=country_finder.get_parent())
        postcode_2 = PageFactory.create_postcode_page(title='Postcode 2', path='11111113',
                                                      parent_page=country_finder.get_parent())

        output = postcode_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderPostcode)
        self.assertNotEquals(postcode_1.title, postcode_2.title)
        self.assertEquals(output.title, postcode_1.title)

    def test_postcode_sibling_finder_returns_postcode_if_multiple_page_types_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=country_finder.get_parent())
        postcode = PageFactory.create_postcode_page(title='Postcode', path='11111113',
                                                    parent_page=country_finder.get_parent())

        output = postcode_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderPostcode)
        self.assertNotEquals(mode_of_study_finder.title, postcode.title)
        self.assertEquals(output.title, postcode.title)

    def test_postcode_sibling_finder_returns_none_if_no_postcode_page_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        output = postcode_sibling_finder(country_finder)
        self.assertIsNone(output)

    def test_summary_sibling_finder_returns_summary_if_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_summary_page(title='Summary', path='11111112',
                                        parent_page=country_finder.get_parent())

        output = summary_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderSummary)

    def test_summary_sibling_finder_returns_first_entry_if_multiple_summary_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        summary_1 = PageFactory.create_summary_page(title='Summary', path='11111112',
                                                    parent_page=country_finder.get_parent())
        summary_2 = PageFactory.create_summary_page(title='Summary 2', path='11111113',
                                                    parent_page=country_finder.get_parent())

        output = summary_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderSummary)
        self.assertNotEquals(summary_1.title, summary_2.title)
        self.assertEquals(output.title, summary_1.title)

    def test_summary_sibling_finder_returns_summary_if_multiple_page_types_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=country_finder.get_parent())
        summary = PageFactory.create_summary_page(title='Summary', path='11111113',
                                                  parent_page=country_finder.get_parent())

        output = summary_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderSummary)
        self.assertNotEquals(mode_of_study_finder.title, summary.title)
        self.assertEquals(output.title, summary.title)

    def test_summary_sibling_finder_returns_none_if_no_summary_page_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        output = summary_sibling_finder(country_finder)
        self.assertIsNone(output)

    def test_results_sibling_finder_returns_results_if_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_results_page(title='Results', path='11111112',
                                        parent_page=country_finder.get_parent())

        output = results_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderResults)

    def test_results_sibling_finder_returns_first_entry_if_multiple_results_in_list(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        results_1 = PageFactory.create_results_page(title='Results', path='11111112',
                                                    parent_page=country_finder.get_parent())
        results_2 = PageFactory.create_results_page(title='Results 2', path='11111113',
                                                    parent_page=country_finder.get_parent())

        output = results_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderResults)
        self.assertNotEquals(results_1.title, results_2.title)
        self.assertEquals(output.title, results_1.title)

    def test_results_sibling_finder_returns_results_if_multiple_page_types_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        mode_of_study_finder = PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder',
                                                                            path='11111112',
                                                                            parent_page=country_finder.get_parent())
        results = PageFactory.create_results_page(title='Results', path='11111113',
                                                  parent_page=country_finder.get_parent())

        output = results_sibling_finder(country_finder)
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderResults)
        self.assertNotEquals(mode_of_study_finder.title, results.title)
        self.assertEquals(output.title, results.title)

    def test_results_sibling_finder_returns_none_if_no_results_page_exists(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        output = results_sibling_finder(country_finder)
        self.assertIsNone(output)


    def test_build_study_mode_filter_when_no_params(self):
        params = []
        expected = ''

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)


    def test_build_study_mode_filter_when_full_and_part_time_selected(self):
        params = ['Full-time', 'Part-time']
        expected = ''

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)        


    def test_build_study_mode_filter_when_full_time_selected(self):
        params = ['Full-time']
        expected = 'full_time'

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)   


    def test_build_study_mode_filter_when_part_time_selected(self):
        params = ['Part-time']
        expected = 'part_time'

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)   


    def test_build_study_mode_filter_when_distance_selected(self):
        params = ['Distance learning']
        expected = 'distance_learning'

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)   


    def test_build_study_mode_filter_when_full_time_and_distance_selected(self):
        params = ['Full-time', 'Distance learning'] 
        expected = 'full_time,distance_learning'

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)   


    def test_build_study_mode_filter_when_part_time_and_distance_selected(self):
        params = ['Part-time', 'Distance learning']    
        expected = 'part_time,distance_learning'

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)   


    def test_build_study_mode_filter_when_full_and_part_time_and_distance_selected(self):
        params = ['Full-time', 'Part-time', 'Distance learning']    
        expected = 'distance_learning'

        actual = build_study_mode_filter(params)
        self.assertEquals(actual, expected)   
