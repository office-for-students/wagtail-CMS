import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CMS.settings.dev")
django.setup()
