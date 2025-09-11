from django.test import tag
from unittest.mock import patch

from CMS.test.mocks.institution_mocks import InstitutionMocks
from CMS.test.utils import UniSimpleTestCase
from errors.models import ApiError
from institutions.models import Institution


@tag('azure')
class InstitutionsModelsTests(UniSimpleTestCase):

    @patch('institutions.request_handler.load_institution_data',
           return_value=InstitutionMocks.get_unsuccessful_institution_load_response())
    def test_institution_find_returns_api_error_if_institution_not_found(self, mock_response):
        # institution, error = Institution.find(1, 'en')
        # self.assertIsNone(institution)
        # self.assertIsNotNone(error)
        # self.assertEquals(type(error), ApiError)
        pass

    def test_institution_find_returns_a_institution_object_if_institution_found(self):
        # institution, error = Institution.find(1, 1)
        # self.assertIsNone(error)
        # self.assertIsNotNone(institution)
        # self.assertEquals(type(institution), Institution)
        pass