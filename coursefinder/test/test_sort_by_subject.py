import unittest

#
# To run all tests in this folder only:
#   python manage.py test coursefinder.test 
#
# To run this test file only:
#   python manage.py test --pattern="test_sort_by_subject.py"
#
class TestSortBySubject(unittest.TestCase):

    def test_failing(self):
        self.assertEqual(1, 2)
