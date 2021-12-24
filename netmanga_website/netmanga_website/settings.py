"""
Django settings for netmanga_website project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
PROJECT_DIR = os.path.join(BASE_DIR,"netmanga_website")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG',0)))
#DEBUG = True

DEV = bool(int(os.getenv('DEV',0)))

ALLOWED_HOSTS = []
if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')  

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'netmanga_website.apps.accounts',
    'netmanga_website.apps.help',
    'netmanga_website.apps.public',
    'storages',
    'fontawesome-free'
]

#Comment out 'whitenoise.middleware.WhiteNoiseMiddleware', during Development
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'log_request_id.middleware.RequestIDMiddleware',
    'csp.middleware.CSPMiddleware',
    'django_permissions_policy.PermissionsPolicyMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


#Security
if(DEV == False):
    #Comment out Redirect when working on heroku free dynos
    #Redirect
    #SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    PREPEND_WWW = True

    #Cookies
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_NAME = '__Secure-sessionid'
    CSRF_COOKIE_NAME = '__Secure-csrftoken'
    


#Content Security Policy
CSP_DEFAULT_SRC = ("'none'",)
CSP_STYLE_SRC = ("'self'",  "'unsafe-inline'", "https://netmanga.s3.amazonaws.com/css/", "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css", "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'",  "'unsafe-eval'", "https://netmanga.s3.amazonaws.com/js/", "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.1.1/chart.min.js", "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js", "https://www.paypal.com/", "https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js")
CSP_IMG_SRC = ("'self'", "'unsafe-eval'", "https://netmanga.s3.amazonaws.com/img/", "https://netmanga.s3.amazonaws.com/", "https://www.redditstatic.com/desktop2x/img/payment-icons/", "https://www.paypal.com/", "https://t.paypal.com/", "data:", "blob:" )
CSP_FONT_SRC = ("'self'", "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/fonts/")
CSP_MEDIA_SRC = ("'self'", "https://netmanga.s3.amazonaws.com/")
CSP_FRAME_SRC = ("'self'", "https://www.paypal.com/")
CSP_CONNECT_SRC = ("'self'", "https://www.paypal.com/xoplatform/logger/api/logger")
CSP_FRAME_ANCESTORS = ("'none'",)


#HTTP Strict Security Transport 
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

#X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True

#Permissions Policy
PERMISSIONS_POLICY = {
    'accelerometer': [],
    #'ambient-light-sensor': [],
    'autoplay': [],
    #'battery': [],
    'camera': [],
    #'cross-origin-isolated': [],
    #'display-capture': [],
    'document-domain': [],
    'encrypted-media': [],
    #'execution-while-not-rendered': [],
    #'execution-while-out-of-viewport': [],
    'fullscreen': [],
    'geolocation': [],
    'gyroscope': [],
    #'interest-cohort' : [],
    'magnetometer': [],
    'microphone': [],
    'midi': [],
    #'navigation-override': [],
    'payment': [],
    #'picture-in-picture': [],
    #'publickey-credentials-get': [],
    #'screen-wake-lock': [],
    #'sync-xhr': [],
    'usb': [],
    #'web-share': [],
    #'xr-spatial-tracking': [],
}

ROOT_URLCONF = 'netmanga_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'netmanga_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST':os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

#Comment out following three lines for development
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if(DEV == False):
    #S3 BUCKETS CONFIG

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION')

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    #STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_ROOT = '/vol/web/static'
    STATIC_URL = '/static/static/'
    # comment out STATICFILES_DIRS in prod
    STATICFILES_DIRS = [   
        os.path.join(BASE_DIR, 'static'),
    ]

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.1/howto/static-files/

    STATIC_URL = '/static/static/'
    # comment out STATICFILES_DIRS in prod
    STATICFILES_DIRS = [   
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_ROOT = '/vol/web/static'

    MEDIA_URL = '/static/media/'

    MEDIA_ROOT = '/vol/web/media'


LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'public:index'
LOGOUT_REDIRECT_URL = 'public:index'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = bool(int(os.getenv('EMAIL_USE_TLS',1)))


LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
LOG_REQUESTS = True

LOGGING = {
    'version': 1,
    'disbale_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s} [%(request_id)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
        },
    },
    'loggers': {
        'log_request_id.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
