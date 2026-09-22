import sys

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

WAGTAILSDOCS_ENABLED = True

STORAGES = {
    "default": {
        "BACKEND": "CMS.storages.azure_storage.AzureMediaStorage",
    },
    "staticfiles": {
        "BACKEND": "CMS.storages.azure_storage.AzureStaticStorage",
    },
}

AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]

STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{os.environ["AZURE_CONTAINER"]}/static/"
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{os.environ["AZURE_CONTAINER"]}/"

# Logging settings

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
        'django.template': {
            'handlers': ['console'],
            'level': 'INFO',  # ignore debug-level template noise
            'propagate': False,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# "uploaded/images"
# Cloudflare

WAGTAILFRONTENDCACHE = {
    'cloudflare': {
        'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
        'EMAIL': os.environ.get('CLOUDFLARE_EMAIL'),
        'API_KEY': os.environ.get('CLOUDFLARE_TOKEN'),
        'ZONEID': os.environ.get('CLOUDFLARE_ZONEID'),
    },
}

# Security settings

SECURE_HSTS_SECONDS = os.environ.get('SECURE_HSTS_SECONDS', 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

try:
    from .local import *
except ImportError:
    pass
