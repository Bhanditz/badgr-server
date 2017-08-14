# settings_local.py is for all instance specific settings

import json

from settings import *
from mainsite import TOP_DIR

with open('/edx/app/badgr/env.json') as env_file:
    ENV_TOKENS = json.load(env_file)

with open('/edx/app/badgr/auth.json') as auth_file:
    AUTH_TOKENS = json.load(auth_file)

DEBUG = ENV_TOKENS.get('DEBUG', False)
TEMPLATE_DEBUG = DEBUG
DEBUG_ERRORS = DEBUG
DEBUG_STATIC = DEBUG
DEBUG_MEDIA = DEBUG

TIME_ZONE = ENV_TOKENS.get('TIME_ZONE', 'America/Los_Angeles')
LANGUAGE_CODE = ENV_TOKENS.get('LANGUAGE_CODE', 'en-us')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(TOP_DIR, 'local.sqlite3'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            "init_command": "SET storage_engine=InnoDB",  # Uncomment when using MySQL to ensure consistency across servers
        },
    }
}
DATABASES = ENV_TOKENS.get('DATABASES', DATABASES)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
        'TIMEOUT': 300,
        'KEY_PREFIX': '',
        'VERSION': 1,
    }
}
CACHES = ENV_TOKENS.get('CACHES', CACHES)



# celery
BROKER_URL = ENV_TOKENS.get('BROKER_URL', 'amqp://localhost:5672/')
CELERY_RESULT_BACKEND = ENV_TOKENS.get('CELERY_RESULT_BACKEND', 'djcelery.backends.cache:CacheBackend')
CELERY_TASK_SERIALIZER = ENV_TOKENS.get('CELERY_TASK_SERIALIZER', 'json')
CELERY_RESULTS_SERIALIZER = ENV_TOKENS.get('CELERY_RESULTS_SERIALIZER', 'json')
CELERY_ACCEPT_CONTENT = ENV_TOKENS.get('CELERY_ACCEPT_CONTENT', ['json'])

HTTP_ORIGIN = ENV_TOKENS.get('HTTP_ORIGIN', 'http://localhost:8000')

# Optionally restrict issuer creation to accounts that have the 'issuer.add_issuer' permission
BADGR_APPROVED_ISSUERS_ONLY = ENV_TOKENS.get('BADGR_APPROVED_ISSUERS_ONLY', True)

# If you have an informational front page outside the Django site that can link back to '/login', specify it here 
ROOT_INFO_REDIRECT = ENV_TOKENS.get('ROOT_INFO_REDIRECT', '/login')

# For the browsable API documentation at '/docs'
# For local development environment: When you have a user you'd like to make API requests, 
# as you can force the '/docs' endpoint to use particular credentials.
# Get a token for your user at '/v1/user/auth-token'
# SWAGGER_SETTINGS = {
#     'api_key': ''
# }


#LTI_OAUTH_CREDENTIALS = {
#    'test': 'secret',
#    'test2': 'reallysecret'
#}

# Run celery tasks in same thread as webserver
CELERY_ALWAYS_EAGER = ENV_TOKENS.get('CELERY_ALWAYS_EAGER', True)


EMAIL_BACKEND = ENV_TOKENS.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
# EMAIL_BACKEND = 'django_ses.SESBackend'

# These are optional -- if they're set as environment variables they won't
# need to be set here as well
# AWS_ACCESS_KEY_ID = AUTH_TOKENS.get('AWS_ACCESS_KEY_ID', '')
# AWS_SECRET_ACCESS_KEY = AUTH_TOKENS.get('AWS_SECRET_ACCESS_KEY, '')

# Your SES account may only be available for one region. You can specify a region, like so:
# AWS_SES_REGION_NAME = AUTH_TOKENS.get('AWS_SES_REGION_NAME', ''us-west-2')
# AWS_SES_REGION_ENDPOINT = AUTH_TOKENS.get('AWS_SES_REGION_ENDPOINT', 'email.us-west-2.amazonaws.com')
# OR:
# AWS_SES_REGION_NAME = 'us-east-1'
# AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

DEFAULT_FROM_EMAIL = ENV_TOKENS.get('DEFAULT_FROM_EMAIL', '')

# debug_toolbar settings
#MIDDLEWARE_CLASSES.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
#INSTALLED_APPS.append('debug_toolbar')
#INTERNAL_IPS = (
#    '127.0.0.1',
#)
#DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}




LOGS_DIR = ENV_TOKENS.get('BADGR_LOG_DIR', os.path.join(TOP_DIR, 'logs'))
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler'
        },

        # badgr events log to disk by default
        'badgr_events': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'badgr_events.log')
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        # Badgr.Events emits all badge related activity
        'Badgr.Events': {
            'handlers': ['badgr_events'],
            'level': 'INFO',
            'propagate': False,

        }

    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'json': {
            '()': 'mainsite.formatters.JsonFormatter',
            'format': '%(asctime)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z',
        }
    },
}

