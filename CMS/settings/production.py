from .base import *

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    'devdiscoveruni.com',
    'www.devdiscoveruni.com',
    'pre-prod-discover-uni.azurewebsites.net',
    'pre-prod-discover-uni-write.azurewebsites.net',
    'discoveruni.org.uk',
    'www.discoveruni.org.uk',
    'production-discover-uni.azurewebsites.net',
    'discoveruni.gov.uk',
    'www.discoveruni.gov.uk',
    'widget.discoveruni.gov.uk',
    'prod-discover-uni.azurewebsites.net',
    'prod-widget-discover-uni.azurewebsites.net',
    'prod-discover-uni-write.azurewebsites.net',
]

# Storage settings

AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER')
MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/"


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL')
WAGTAILADMIN_NOTIFICATION_USE_HTML = True
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False


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
