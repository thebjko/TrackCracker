from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.getenv('DB_NAME'),
    'USER': os.getenv('USERNAME'),
    'PASSWORD': os.getenv('PASSWORD'),
    'HOST': os.getenv('HOSTNAME'),
    'PORT': os.getenv('RDS_PORT'),
    'OPTIONS': {
        'sql_mode': 'STRICT_ALL_TABLES'
    },
}