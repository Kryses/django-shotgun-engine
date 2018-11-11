from django_shotgun_engine.base import DatabaseWrapper
from django.conf import settings
from utils import TestCase




class ShotgunTest(TestCase):
    def test_database_wrapper_connect(self):
        wrapper = DatabaseWrapper(settings)
        wrapper.connect()
        print wrapper.connection
