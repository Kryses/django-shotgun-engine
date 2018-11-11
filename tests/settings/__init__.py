from settings_base import *
from .shotgun import *

DEFAULT_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
]

INSTALLED_APPS = [
    'django_shotgun_engine',
    'shotgun'
]

TEST_RUNNER = 'tests.test_runners.ShotgunTestSuiteRunner'

DATABASE_ROUTERS = ['django_shotgun_engine.router.ShotgunRouter']

try:
    from tests.shotgun_local_settings import *
except ImportError:
    pass