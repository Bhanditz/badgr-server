"""
Module for code that should run during Badgr server startup
"""

import django
from django.conf import settings

# Force settings to run so that the python path is modified

settings.INSTALLED_APPS  # pylint: disable=pointless-statement


def run():
    """
    Executed during django startup
    """
    django.setup()
