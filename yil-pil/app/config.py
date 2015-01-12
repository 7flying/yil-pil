import os
import urlparse

DEBUG = False
MANAGER_DEBUG = False
API_DEBUG = False

WTF_CSRF_ENABLED = False

# Pagination
API_PAGINATION = 5

# Max number of last updates
API_MAX_UPDATES = 30

# Database stuff
REDIS_URL = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost'))
REDIS_HOST = REDIS_URL.hostname
REDIS_PORT = '6379' if REDIS_HOST == 'localhost' else REDIS_URL.port
REDIS_DB = 0
REDIS_PASSWORD = None if REDIS_HOST == 'localhost' else REDIS_URL.password

# Sec
SECRET_KEY = os.environ.get('SECRET_KEY') or 'super hard to guess secret string'
SSL_DISABLE = bool(os.environ.get('SSL_DISABLE', True))
