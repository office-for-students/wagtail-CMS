from .base import *

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# NOTE: this SECRET_KEY is ONLY used in testing, NOT used in production
SECRET_KEY = '3z@sut7t&=hkx9*+b-h=&2$_ajcqvqrfcc0mc@*)y6c5v#6qsz'

try:
    from .local import *
except ImportError:
    pass
