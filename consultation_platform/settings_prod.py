from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update ALLOWED_HOSTS with your Windows machine's IP or domain
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-windows-ip-here', '188.247.244.153', 'sosbebe-mobile.crmonline.ro']

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = '/root/flowBackend/staticfiles/'

# Database settings (you can use SQLite for simplicity, or configure PostgreSQL/MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
} 