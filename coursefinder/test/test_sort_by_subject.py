from coursefinder.sort_by_subject import SortBySubject
import unittest

#
# To run all tests in this folder only:
#   python manage.py test coursefinder.test 
#
# To run this test file only:
#   python manage.py test --pattern="test_sort_by_subject.py"
#
class TestGetLabelForSubject(unittest.TestCase):

    def test_convert_to_dictionary(self):
        actual = SortBySubject.convert_to_dictionary(self, data)        
        self.assertEqual(actual, expected)
        self.assertEquals(actual['CAH17-01-08']['english_name'], 'Accounting')
        self.assertEquals(actual['CAH02-04-02']['welsh_name'], 'Nyrsio oedolion')

    def test_when_no_subject_found_return_None(self):
        subject = 'something-that-does-not-exist'
        actual = SortBySubject(data).get_labels(subject)
        expected = None
        self.assertEqual(actual, expected)
        
    def test_when_subject_found_return_labels(self):
        subject = 'CAH02-04-02'
        actual = SortBySubject(data).get_labels(subject)
        self.assertEqual(actual['english_name'], 'Adult nursing')
        self.assertEqual(actual['welsh_name'], 'Nyrsio oedolion')

    def test_when_subject_found_return_english_label(self):
        subject = 'CAH17-01-08'
        actual = SortBySubject(data).get_label(subject)
        self.assertEqual(actual, 'Accounting')

    def test_when_subject_found_return_welsh_label(self):
        subject = 'CAH17-01-08'
        actual = SortBySubject(data).get_label_welsh(subject)
        self.assertEqual(actual, 'Cyfrifeg')

data = [
    {
        "code": "CAH17-01-08",
        "english_name": "Accounting",
        "welsh_name": "Cyfrifeg",
        "level": "3"
    },
    {
        "code": "CAH02-04-02",
        "english_name": "Adult nursing",
        "welsh_name": "Nyrsio oedolion",
        "level": "3"
    }
]

expected = {
   "CAH17-01-08":{
      "english_name":"Accounting",
      "welsh_name":"Cyfrifeg",
   },
   "CAH02-04-02":{
      "english_name":"Adult nursing",
      "welsh_name":"Nyrsio oedolion",
   }
}
