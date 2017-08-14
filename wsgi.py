"""
WSGI config for Badgr server.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments.
It exposes a module-level variable named ``application``. Django's
``runserver`` and ``runfcgi`` commands discover this application via the
``WSGI_APPLICATION`` setting.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.mainsite.settings_local")

from apps.mainsite import startup
startup.run()

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()  # pylint: disable=invalid-name
