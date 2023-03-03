import os

AUTH_USER_MODEL='mainapp.User'
NUMBER_GROUPING = 3

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
if SETTINGS_MODULE == 'settings.local':
    from settings.local import *
elif SETTINGS_MODULE == 'settings.deploy':
    from settings.deploy import *
else:
    raise ValueError('Unknown DJANGO_SETTINGS_MODULE: {}'.format(SETTINGS_MODULE))


STRIPE_ENDPOINT_SECRET = os.environ['STRIPE_ENDPOINT_SECRET']


