from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL = os.environ.get('LOCAL', False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3z@sut7t&=hkx9*+b-h=&2$_ajcqvqrfcc0mc@*)y6c5v#6qsz'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
