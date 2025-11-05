from .base import *

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# NOTE: this SECRET_KEY is ONLY used in testing, NOT used in production
SECRET_KEY = '3z@sut7t&=hkx9*+b-h=&2$_ajcqvqrfcc0mc@*)y6c5v#6qsz'

try:
    from .local import *
except ImportError:
    pass
