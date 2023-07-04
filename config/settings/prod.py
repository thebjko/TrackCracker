from .base import *


import boto3

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
print(os.getenv('SECRET_KEY'))
print(os.getenv('DB_NAME'))
print(os.getenv('USERNAME'))
print(os.getenv('HOSTNAME'))
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

AWS_STORAGE_BUCKET_NAME = "supertodo-bucket-2023"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.ap-northeast-2.amazonaws.com"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
