from unittest.mock import patch

from CMS.test.mocks import CourseMocks
from CMS.test.utils import UniSimpleTestCase
from courses.models import SatisfactionBlock, EntryInformationBlock, AfterOneYearBlock, EarningsAfterCourseBlock, \
    AccreditationBlock, Course
from errors.models import ApiError


class CoursesModelsTests(UniSimpleTestCase):

    def test_SatisfactionBlock_returns_student_satisfaction_data_set_value(self):
        satisfaction_block = SatisfactionBlock().meta.value_class
        self.assertEquals(satisfaction_block.data_set(), 'student_satisfaction')

    def test_EntryInformationBlock_returns_entry_information_data_set_value(self):
        entry_block = EntryInformationBlock().meta.value_class
        self.assertEquals(entry_block.data_set(), 'entry_information')

    def test_AfterOneYearBlock_returns_after_one_year_data_set_value(self):
        one_year_block = AfterOneYearBlock().meta.value_class
        self.assertEquals(one_year_block.data_set(), 'after_one_year')

    def test_AfterCourseBlock_returns_after_the_course_data_set_value(self):
        after_course_block = EarningsAfterCourseBlock().meta.value_class
        self.assertEquals(after_course_block.data_set(), 'earnings_after_the_course')

    def test_AccreditationBlock_returns_professional_accreditation_data_set_value(self):
        accreditation_block = AccreditationBlock().meta.value_class
        self.assertEquals(accreditation_block.data_set(), 'professional_accreditation')

    @patch('courses.request_handler.load_course_data', return_value=CourseMocks.get_unsuccessful_course_load_response())
    def test_course_find_returns_api_error_if_course_not_found(self, mock_response):
        course, error = Course.find(1, 1, 1, 'en')
        self.assertIsNone(course)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), ApiError)

    def test_course_find_returns_a_course_object_if_course_found(self):
        course, error = Course.find(1, 1, 1, 'en')
        self.assertIsNone(error)
        self.assertIsNotNone(course)
        self.assertEquals(type(course), Course)
