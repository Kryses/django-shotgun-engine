DATABASES = {
    'default': {
        'ENGINE': 'django_shotgun_engine',
        'NAME': 'test',
        'OPTIONS': {'OPERATIONS': {}}
    },
}

SERIALIZATION_MODULES = {'json': 'settings.serializer'}

SECRET_KEY = 'super secret'



try:
    from local_settings import *
except ImportError:
    pass