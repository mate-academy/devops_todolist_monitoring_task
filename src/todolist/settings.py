"""
Django settings for todolist project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from todolist.customlogger import PrometheusLogHandler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGING = {
    'version': 1,  # Specifies the logging configuration schema version
    'disable_existing_loggers': False,  # Keep default Django loggers active
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',  # Use `{}` to format log messages
        },
    },
    'handlers': {
        'file': {  # Write logs to a file
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'app.log'),  # Log file path
            'formatter': 'verbose',  # Use the verbose format
        },
        'prometheus': {  # Send logs to Prometheus (custom handler)
            'level': 'INFO',
            'class': 'todolist.customlogger.PrometheusLogHandler',  # Our custom handler
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'prometheus'],  # Use both file and Prometheus handlers
            'level': 'INFO',  # Log everything INFO and above
            'propagate': True,  # Pass log messages to parent loggers
        },
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "todolist",
    "lists",
    "accounts",
    "rest_framework",
    "api",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "todolist.urls"

WSGI_APPLICATION = "todolist.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DB_NAME = os.environ.get("DB_NAME", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "")

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,  # You can use a different host if your MySQL server is on a remote machine.
        'PORT': '',  # Leave this empty to use the default MySQL port (3306).
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = "/static/"


# Login settings

LOGIN_URL = "/auth/login/"

LOGOUT_URL = "/auth/logout/"


# rest (api) framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    },
]
