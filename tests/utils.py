from django.conf import settings
from django.test import TestCase


class TestCase(TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        if getattr(settings, 'TEST_DEBUG', False):
            settings.DEBUG = True

    def assertEqualLists(self, a, b):
        self.assertEqual(list(a), list(b))
