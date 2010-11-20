from default_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Kevin Lloyd', 'kev@lloydie.co.uk'),
    ('Ben Burry', 'ben@burry.name'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'moocraft',                      # Or path to database file if using sqlite3.
        'USER': 'moocraft',                      # Not used with sqlite3.
        'PASSWORD': 'punchingtrees',                  # Not used with sqlite3.
        'HOST': 'mysql.moocraft.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MEDIA_ROOT = '/home/moocraft/moocraft.com/public/media'
SECRET_KEY = '4e^7excr$9$60=k1(l)&d@50og3dy+nw6lk+dl_am5&30$6^%^'

MOO_CONSUMER_KEY=
MOO_CONSUMER_SECRET=
