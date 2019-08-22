from CMS.test.utils import UniSimpleTestCase


class MedexTestUtilsTests(UniSimpleTestCase):

    def test_uni_simple_test_case_assert_is_true_returns_true_when_passed_true(self):
        self.assertIsTrue(True)

    def test_uni_simple_test_case_assert_is_true_returns_false_when_passed_false(self):
        try:
            self.assertIsTrue(False)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_true_returns_false_when_passed_a_truthy_value(self):
        try:
            truthy_variable = 'A string'
            self.assertIsTrue(truthy_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_true_returns_false_when_passed_a_falsey_value(self):
        try:
            falsey_variable = None
            self.assertIsTrue(falsey_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_false_returns_true_when_passed_false(self):
        self.assertIsFalse(False)

    def test_uni_simple_test_case_assert_is_false_returns_false_when_passed_true(self):
        try:
            self.assertIsFalse(True)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_false_returns_false_when_passed_a_truthy_value(self):
        try:
            truthy_variable = 'A string'
            self.assertIsFalse(truthy_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_false_returns_false_when_passed_a_falsey_value(self):
        try:
            falsey_variable = None
            self.assertIsFalse(falsey_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_none_returns_true_when_passed_none(self):
        self.assertIsNone(None)

    def test_uni_simple_test_case_assert_is_none_returns_false_when_passed_something_other_than_none(self):
        try:
            self.assertIsNone("test")

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_not_none_returns_true_when_not_passed_something_other_than_none(self):
        self.assertIsNotNone('Anything that is not none')

    def test_uni_simple_test_case_assert_is_not_none_returns_false_when_passed_none(self):
        try:
            self.assertIsNone(None)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_get_context_value_loads_the_correct_value_for_a_valid_key(self):
        key = 'testKey'
        value = 'A short test string'
        context = {
            key: value,
        }
        result = self.get_context_value(context, key)
        self.assertEqual(result, value)

    def test_get_context_value_throws_a_key_error_when_passed_an_invalid_key(self):
        key = 'testKey'
        value = 'A short test string'
        invalidKey = 'wrongKey'
        context = {
            key: value,
        }
        try:
            self.get_context_value(context, invalidKey)
            self.assertFalse('Test failed to produce expected key error')
        except KeyError:
            self.assertTrue('Test produced expected key error')
