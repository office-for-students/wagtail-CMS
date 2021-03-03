from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

SECRET_KEY = "y%_whg_blbor4(6e!j3qxin9_qma025j+u=mn27%u^pdw=n2b%"

try:
    from .local import *
except ImportError:
    pass
