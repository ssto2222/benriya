import os

AUTH_USER_MODEL='mainapp.User'
NUMBER_GROUPING = 3

if 'AWS' in os.environ:
    from settings.deploy import *
from settings.local import *



STRIPE_ENDPOINT_SECRET = os.environ['STRIPE_ENDPOINT_SECRET']


