from unittest.mock import patch

from CMS.test.factories import PageFactory
from CMS.test.mocks import SearchMocks
from CMS.test.utils import UniSimpleTestCase
from coursefinder.models import CourseSearch, CourseFinderChooseCountry, CourseFinderModeOfStudy, \
    CourseFinderChooseSubject, CourseFinderNarrowSearch, CourseFinderPostcode, CourseFinderSummary, CourseFinderResults, \
    CourseFinderLandingPage
from coursefinder.utils import choose_country_sibling_finder, mode_of_study_sibling_finder, \
    choose_subject_sibling_finder, narrow_search_sibling_finder, postcode_sibling_finder, summary_sibling_finder, \
    results_sibling_finder
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

    def test_course_finder_choose_country_next_page_returns_mode_of_study_sibling(self):
        country_finder = PageFactory.create_country_finder_page(title='Country Finder')
        PageFactory.create_mode_of_study_finder_page(title='Mode of Study Finder', path='11111112',
                                                     parent_page=country_finder.get_parent())

        self.assertIsNotNone(country_finder.next_page)
        self.assertEquals(type(country_finder.next_page), CourseFinderModeOfStudy)

    def test_course_finder_choose_country_back_page_returns_parent_page(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        country_finder = PageFactory.create_country_finder_page(title='Country Finder', parent_page=course_finder_page)

        self.assertIsNotNone(country_finder.back_page)
        self.assertEquals(type(country_finder.back_page), CourseFinderLandingPage)

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

    def test_course_finder_town_city_next_page_returns_summary_sibling(self):
        town_city = PageFactory.create_town_city_page(title='Town City')
        PageFactory.create_summary_page(title='Summary', path='11111112',
                                        parent_page=town_city.get_parent())

        self.assertIsNotNone(town_city.next_page)
        self.assertEquals(type(town_city.next_page), CourseFinderSummary)

    def test_course_finder_town_city_back_page_returns_narrow_search_sibling(self):
        town_city = PageFactory.create_town_city_page(title='Town City')
        PageFactory.create_narrow_search_page(title='Narrow Search', path='11111112',
                                              parent_page=town_city.get_parent())

        self.assertIsNotNone(town_city.back_page)
        self.assertEquals(type(town_city.back_page), CourseFinderNarrowSearch)

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

    def test_course_finder_summary_back_page_returns_postcode_sibling(self):
        summary = PageFactory.create_summary_page(title='Summary')
        PageFactory.create_postcode_page(title='Postcode', path='11111112', parent_page=summary.get_parent())

        self.assertIsNotNone(summary.back_page)
        self.assertEquals(type(summary.back_page), CourseFinderPostcode)


class CourseFinderUtilsTests(UniSimpleTestCase):
    def test_choose_country_sibling_finder_returns_country_finder_if_in_list(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
        PageFactory.create_country_finder_page(title='Country Finder', parent_page=course_finder_page)

        output = choose_country_sibling_finder(course_finder_page.get_children().specific())
        self.assertIsNotNone(output)
        self.assertEquals(type(output), CourseFinderChooseCountry)

    def test_choose_country_sibling_finder_returns_first_entry_if_multiple_country_finders_in_list(self):
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
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
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
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
        course_finder_page = PageFactory.create_course_finder_landing_page('Course Finder')
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
