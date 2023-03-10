import os

AUTH_USER_MODEL='mainapp.User'
NUMBER_GROUPING = 3

from settings.local import *



STRIPE_ENDPOINT_SECRET = os.environ['STRIPE_ENDPOINT_SECRET']


