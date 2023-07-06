from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-59lmck$$l!9q974mx7*nc&m2y^_k#e3dz&7nub(cmwark#n(d5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

if 'MYSQL_PASSWORD' in os.environ and 'MYSQL_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DB_NAME'),
            'USER': 'root',
            'PASSWORD': os.getenv('MYSQL_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }