import sys

from .base import *

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    'testdiscoveruni.com',
    'www.testdiscoveruni.com',
    'pre-prod-discover-uni.azurewebsites.net',
    'discoveruni.org.uk',
    'www.discoveruni.org.uk',
    'production-discover-uni.azurewebsites.net',
    'discoveruni.gov.uk',
    'www.discoveruni.gov.uk',
    'prod-discover-uni.azurewebsites.net'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
