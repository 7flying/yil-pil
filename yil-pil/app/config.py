import os

DEBUG = True
MANAGER_DEBUG = False
API_DEBUG = False

WTF_CSRF_ENABLED = False

# Pagination
API_PAGINATION = 5

# Max number of last updates
API_MAX_UPDATES = 30

# Database stuff
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = 0

# Sec
SECRET_KEY = os.environ.get('SECRET_KEY') or 'super hard to guess secret string'
