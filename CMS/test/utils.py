from django.test import SimpleTestCase


class UniSimpleTestCase(SimpleTestCase):

    def assertIsTrue(self, value):
        self.assertIs(value, True)

    def assertIsFalse(self, value):
        self.assertIs(value, False)

    def assertIsNone(self, value):
        self.assertIsTrue(value is None)

    def assertIsNotNone(self, value):
        self.assertIsTrue(value is not None)

    def get_context_value(self, context, key):
        return context[key]
