"""
Django settings for the redirectioneaza project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import hashlib
import os
from base64 import urlsafe_b64encode
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import environ
import sentry_sdk
from cryptography.fernet import Fernet
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from localflavor.ro.ro_counties import COUNTIES_CHOICES

# Constants for memory sizes
KIBIBYTE = 1024
MEBIBYTE = KIBIBYTE * 1024
GIBIBYTE = MEBIBYTE * 1024
TEBIBYTE = GIBIBYTE * 1024

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT = Path(__file__).resolve().parent.parent.parent
BASE_DIR = os.path.abspath(os.path.join(ROOT, "backend"))

ENV_FILE_NAME = os.environ.get("ENV_FILE_NAME", ".env.local")
ENV_FILE_PATH = os.path.join(BASE_DIR, os.pardir, ENV_FILE_NAME)

env = environ.Env(
    # set casting, default value
    # Django settings
    DEBUG=(bool, False),
    ENVIRONMENT=(str, "production"),
    DATA_UPLOAD_MAX_NUMBER_FIELDS=(int, 1000),
    OLD_SESSION_KEY=(str, ""),
    LOG_LEVEL=(str, "WARNING"),
    ENABLE_CACHE=(bool, True),
    ENABLE_FORMS_DOWNLOAD=(bool, True),
    TIMEDELTA_FORMS_DOWNLOAD_MINUTES=(int, 360),
    TIMEDELTA_DONATIONS_LIMIT_DOWNLOAD_DAYS=(int, 31),
    IS_CONTAINERIZED=(bool, False),
    RECAPTCHA_ENABLED=(bool, True),
    # proxy headers
    USE_PROXY_FORWARDED_HOST=(bool, False),
    PROXY_SSL_HEADER=(str, "HTTP_CLOUDFRONT_FORWARDED_PROTO"),
    # db settings
    DATABASE_ENGINE=(str, "sqlite3"),
    DATABASE_NAME=(str, "default"),
    DATABASE_USER=(str, "root"),
    DATABASE_PASSWORD=(str, ""),
    DATABASE_HOST=(str, "localhost"),
    DATABASE_PORT=(str, "3306"),
    # site settings
    APEX_DOMAIN=(str, "redirectioneaza.ro"),
    BASE_WEBSITE=(str, "https://redirectioneaza.ro"),
    SITE_TITLE=(str, "redirectioneaza.ro"),
    DONATIONS_LIMIT_DAY=(int, 25),
    DONATIONS_LIMIT_MONTH=(int, 5),
    DONATIONS_LIMIT_YEAR=(int, 2016),
    DONATIONS_LIMIT_TO_CURRENT_YEAR=(bool, True),
    DONATIONS_XML_LIMIT_PER_FILE=(int, 100),
    # security settings
    ALLOWED_HOSTS=(list, ["*"]),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOW_ALL_ORIGINS=(bool, False),
    # email settings
    EMAIL_SEND_METHOD=(str, "async"),
    EMAIL_BACKEND=(str, "django.core.mail.backends.console.EmailBackend"),
    EMAIL_HOST=(str, ""),
    EMAIL_PORT=(str, ""),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    EMAIL_USE_TLS=(str, ""),
    EMAIL_FAIL_SILENTLY=(bool, False),
    CONTACT_EMAIL_ADDRESS=(str, "redirectioneaza@code4.ro"),
    DEFAULT_FROM_EMAIL=(str, "no-reply@code4.ro"),
    NO_REPLY_EMAIL=(str, "no-reply@code4.ro"),
    # django-q2 settings
    DJANGO_Q_WORKERS_COUNT=(int, 1),
    DJANGO_Q_RECYCLE_RATE=(int, 100),
    DJANGO_Q_TIMEOUT_SECONDS=(int, 900),  # A task must finish in less than 15 minutes
    DJANGO_Q_RETRY_AFTER_TIMEOUT_SECONDS=(int, 300),  # Retry unfinished tasks 5 minutes after timeout
    DJANGO_Q_POLL_SECONDS=(int, 4),
    IMPORT_METHOD=(str, "async"),
    IMPORT_USE_BATCHES=(bool, True),
    IMPORT_BATCH_SIZE=(int, 100),
    # recaptcha settings
    CAPTCHA_PUBLIC_KEY=(str, ""),
    CAPTCHA_PRIVATE_KEY=(str, ""),
    CAPTCHA_REQUIRED_SCORE=(float, 0.5),
    CAPTCHA_VERIFY_URL=(str, "https://www.google.com/recaptcha/api/siteverify"),
    CAPTCHA_POST_PARAM=(str, "g-recaptcha-response"),
    # aws settings
    AWS_REGION_NAME=(str, ""),
    # S3
    USE_S3=(bool, False),
    AWS_S3_REGION_NAME=(str, ""),
    AWS_S3_SIGNATURE_VERSION=(str, "s3v4"),
    AWS_S3_ADDRESSING_STYLE=(str, "virtual"),
    AWS_S3_STORAGE_DEFAULT_BUCKET_NAME=(str, ""),
    AWS_S3_STORAGE_PUBLIC_BUCKET_NAME=(str, ""),
    AWS_S3_STORAGE_STATIC_BUCKET_NAME=(str, ""),
    AWS_S3_DEFAULT_ACL=(str, "private"),
    AWS_S3_PUBLIC_ACL=(str, ""),
    AWS_S3_STATIC_ACL=(str, ""),
    AWS_S3_DEFAULT_PREFIX=(str, ""),
    AWS_S3_PUBLIC_PREFIX=(str, ""),
    AWS_S3_STATIC_PREFIX=(str, ""),
    AWS_S3_DEFAULT_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_PUBLIC_CUSTOM_DOMAIN=(str, ""),
    AWS_S3_STATIC_CUSTOM_DOMAIN=(str, ""),
    # SES
    AWS_SES_REGION_NAME=(str, ""),
    AWS_SES_USE_V2=(bool, True),
    AWS_SES_CONFIGURATION_SET_NAME=(str, None),
    AWS_SES_AUTO_THROTTLE=(float, 0.5),
    AWS_SES_REGION_ENDPOINT=(str, ""),
    # Cognito
    AWS_COGNITO_DOMAIN=(str, ""),
    AWS_COGNITO_CLIENT_ID=(str, ""),
    AWS_COGNITO_CLIENT_SECRET=(str, ""),
    AWS_COGNITO_USER_POOL_ID=(str, ""),
    AWS_COGNITO_REGION=(str, ""),
    # NGO Hub
    NGOHUB_HOME_HOST=(str, "ngohub.ro"),
    NGOHUB_APP_HOST=(str, "app-staging.ngohub.ro"),
    NGOHUB_API_HOST=(str, "api-staging.ngohub.ro"),
    NGOHUB_API_ACCOUNT=(str, ""),
    NGOHUB_API_KEY=(str, ""),
    UPDATE_ORGANIZATION_METHOD=(str, "async"),
    # sentry
    SENTRY_DSN=(str, ""),
    SENTRY_TRACES_SAMPLE_RATE=(float, 0),
    SENTRY_PROFILES_SAMPLE_RATE=(float, 0),
    # Google Analytics:
    GOOGLE_ANALYTICS_ID=(str, ""),
    # App settings
    ENABLE_FULL_CUI_VALIDATION=(bool, True),
)

environ.Env.read_env(ENV_FILE_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret
SECRET_KEY = env.str("SECRET_KEY")
SECRET_KEY_HASH = hashlib.blake2s(SECRET_KEY.encode()).hexdigest()
OLD_SESSION_KEY = env.str("OLD_SESSION_KEY")

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = env.bool("DEBUG")
ENVIRONMENT = env.str("ENVIRONMENT")

DATA_UPLOAD_MAX_NUMBER_FIELDS = env.int("DATA_UPLOAD_MAX_NUMBER_FIELDS")

# Proxy HOST & Scheme headers
USE_X_FORWARDED_HOST = env.bool("USE_PROXY_FORWARDED_HOST", False)
if proxy_ssl_header_name := env.str("PROXY_SSL_HEADER", ""):
    SECURE_PROXY_SSL_HEADER = (proxy_ssl_header_name, "https")

# superuser/admin seed data
DJANGO_ADMIN_PASSWORD = env.str("DJANGO_ADMIN_PASSWORD", None)
DJANGO_ADMIN_EMAIL = env.str("DJANGO_ADMIN_EMAIL", None)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
APEX_DOMAIN = env.str("APEX_DOMAIN")
BASE_WEBSITE = env.str("BASE_WEBSITE")

CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS")

# Application definition
APPEND_SLASH = True

# some settings will be different if it's not running in a container (e.g., locally, on a Mac)
IS_CONTAINERIZED = env.bool("IS_CONTAINERIZED")

DEFAULT_REVISION_STRING = "dev"

VERSION = env.str("VERSION", "edge")
REVISION = env.str("REVISION", DEFAULT_REVISION_STRING)
REVISION = REVISION[:7]

if IS_CONTAINERIZED and VERSION == "edge" and REVISION == DEFAULT_REVISION_STRING:
    version_file = "/var/www/redirect/.version"
    if os.path.exists(version_file):
        with open(version_file) as f:
            VERSION, REVISION = f.read().strip().split("+")

VERSION_SUFFIX = f"{VERSION}+{REVISION}"
VERSION_LABEL = f"redirect@{VERSION_SUFFIX}"


# Sentry
ENABLE_SENTRY = True if env.str("SENTRY_DSN") else False
if ENABLE_SENTRY:
    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE"),
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE"),
        environment=ENVIRONMENT,
        release=VERSION_LABEL,
    )


# Logging
DJANGO_LOG_LEVEL = env.str("LOG_LEVEL").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": DJANGO_LOG_LEVEL,
    },
}

# Application definition

INSTALLED_APPS = [
    "unfold",  # this must be loaded before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps:
    "storages",
    "django_q",
    "django_recaptcha",
    # authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.amazon_cognito",
    # custom apps:
    "donations",
    "partners",
    "users",
    "importer",
]

if not env.bool("USE_S3"):
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "partners.middleware.PartnerDomainMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # this is the default
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "redirectioneaza.urls"

TEMPLATES = [
    {
        # New templates for v2
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.abspath(os.path.join(BASE_DIR, "templates", "v2")),
            os.path.abspath(os.path.join(BASE_DIR, "templates", "v3")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "partners.context_processors.custom_subdomain",
                "users.context_processors.is_admin",
                "donations.context_processors.default_ngo_logo",
            ],
        },
    },
    {
        # The original v1 templates which use the Jinja engine
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.abspath(os.path.join(BASE_DIR, "templates", "v1"))],
        "APP_DIRS": False,
        "OPTIONS": {
            "environment": "redirectioneaza.jinja2.environment",
            "context_processors": [
                "partners.context_processors.custom_subdomain",
                "users.context_processors.is_admin",
                "donations.context_processors.default_ngo_logo",
            ],
        },
    },
]

WSGI_APPLICATION = "redirectioneaza.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASE_ENGINE = env("DATABASE_ENGINE")

REMOTE_DATABASE_ENGINES = {
    "mysql": "django.db.backends.mysql",
    "postgres": "django.db.backends.postgresql",
}
if DATABASE_ENGINE in REMOTE_DATABASE_ENGINES.keys():
    DATABASES = {
        "default": {
            "ENGINE": REMOTE_DATABASE_ENGINES[DATABASE_ENGINE],
            "NAME": env("DATABASE_NAME"),
            "USER": env("DATABASE_USER"),
            "PASSWORD": env("DATABASE_PASSWORD"),
            "HOST": env("DATABASE_HOST"),
            "PORT": env("DATABASE_PORT"),
        }
    }
else:
    # create a sqlite database in the .db_sqlite directory
    sqlite_path = Path(os.path.join(BASE_DIR, ".db_sqlite", "db.sqlite3"))

    if not sqlite_path.exists():
        sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite_path.open("w") as f:
            pass

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.abspath(sqlite_path),
        }
    }

CACHE_TIMEOUT_TINY = 60 * 3
CACHE_TIMEOUT_SMALL = 60 * 60
CACHE_TIMEOUT_MEDIUM = 60 * 60 * 24
CACHE_TIMEOUT_LARGE = 60 * 60 * 24 * 7
CACHE_TIMEOUT_EXTRA_LARGE = 60 * 60 * 24 * 30

ENABLE_CACHE = env.bool("ENABLE_CACHE")
if ENABLE_CACHE:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "redirect_cache_default",
            "TIMEOUT": CACHE_TIMEOUT_SMALL,  # default cache timeout in seconds
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

TIMEOUT_CACHE_SHORT = 60  # 1 minute
TIMEOUT_CACHE_NORMAL = 60 * 15  # 15 minutes
TIMEOUT_CACHE_LONG = 60 * 60 * 2  # 2 hours

# User & Auth
AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Email settings
EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_SEND_METHOD = env.str("EMAIL_SEND_METHOD")

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
NO_REPLY_EMAIL = env.str("NO_REPLY_EMAIL")

EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.str("EMAIL_PORT")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

EMAIL_FAIL_SILENTLY = env.bool("EMAIL_FAIL_SILENTLY")

if EMAIL_BACKEND == "django_ses.SESBackend":
    AWS_SES_CONFIGURATION_SET_NAME = env.str("AWS_SES_CONFIGURATION_SET_NAME")

    AWS_SES_AUTO_THROTTLE = env.float("AWS_SES_AUTO_THROTTLE", default=0.5)
    AWS_SES_REGION_NAME = env.str("AWS_SES_REGION_NAME") if env("AWS_SES_REGION_NAME") else env("AWS_REGION_NAME")
    AWS_SES_REGION_ENDPOINT = env.str("AWS_SES_REGION_ENDPOINT", default=f"email.{AWS_SES_REGION_NAME}.amazonaws.com")

    AWS_SES_FROM_EMAIL = DEFAULT_FROM_EMAIL

    USE_SES_V2 = env.bool("AWS_SES_USE_V2", default=True)

    if aws_access_key := env("AWS_ACCESS_KEY_ID", default=None):
        AWS_ACCESS_KEY_ID = aws_access_key
        AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
else:
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ro"

TIME_ZONE = "Europe/Bucharest"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Media & Static files storage
# https://docs.djangoproject.com/en/4.2/howto/static-files/

static_static_location = "static"
public_media_location = "media"
private_media_location = "media"

static_storage = "whitenoise.storage.CompressedStaticFilesStorage"
media_storage = "django.core.files.storage.FileSystemStorage"

STATIC_URL = f"{static_static_location}/"
MEDIA_URL = f"{public_media_location}/"

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "static"))
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "media"))

DEV_DEPENDECIES_LOCATION = "bower_components"

STATICFILES_DIRS = [
    os.path.abspath(os.path.join(DEV_DEPENDECIES_LOCATION)),
    os.path.abspath(os.path.join("static_extras")),
]

default_storage_options = {}

public_storage_options = {}
static_storage_options = {}

if env.bool("USE_S3"):
    media_storage = "storages.backends.s3boto3.S3Boto3Storage"
    static_storage = "storages.backends.s3boto3.S3StaticStorage"

    # https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
    default_storage_options = {
        "bucket_name": env.str("AWS_S3_STORAGE_DEFAULT_BUCKET_NAME"),
        "default_acl": env.str("AWS_S3_DEFAULT_ACL"),
        "region_name": env.str("AWS_S3_REGION_NAME") or env.str("AWS_REGION_NAME"),
        "object_parameters": {"CacheControl": "max-age=86400"},
        "file_overwrite": False,
        "signature_version": env.str("AWS_S3_SIGNATURE_VERSION"),
        "addressing_style": env.str("AWS_S3_ADDRESSING_STYLE"),
    }

    # Authentication, if not using IAM roles
    if aws_session_profile := env.str("AWS_S3_SESSION_PROFILE", default=None):
        default_storage_options["session_profile"] = aws_session_profile
    elif aws_access_key := env.str("AWS_ACCESS_KEY_ID", default=None):
        default_storage_options["access_key"] = aws_access_key
        default_storage_options["secret_key"] = env.str("AWS_SECRET_ACCESS_KEY")

    # Additional default configurations
    if default_prefix := env.str("AWS_S3_DEFAULT_PREFIX", default=None):
        default_storage_options["location"] = default_prefix
    if custom_domain := env.str("AWS_S3_DEFAULT_CUSTOM_DOMAIN", default=None):
        public_storage_options["custom_domain"] = custom_domain

    # Public storage options
    public_storage_options = deepcopy(default_storage_options)
    if public_acl := env.str("AWS_S3_PUBLIC_ACL"):
        public_storage_options["default_acl"] = public_acl
    if public_bucket_name := env.str("AWS_S3_STORAGE_PUBLIC_BUCKET_NAME"):
        public_storage_options["bucket_name"] = public_bucket_name
    if public_prefix := env.str("AWS_S3_PUBLIC_PREFIX", default=None):
        public_storage_options["location"] = public_prefix
    if custom_domain := env.str("AWS_S3_PUBLIC_CUSTOM_DOMAIN", default=None):
        public_storage_options["custom_domain"] = custom_domain

    static_storage_options = deepcopy(public_storage_options)
    if static_acl := env.str("AWS_S3_STATIC_ACL"):
        static_storage_options["default_acl"] = static_acl
    if static_bucket_name := env.str("AWS_S3_STORAGE_STATIC_BUCKET_NAME"):
        static_storage_options["bucket_name"] = static_bucket_name
    if static_prefix := env.str("AWS_S3_STATIC_PREFIX", default=None):
        static_storage_options["location"] = static_prefix
    if custom_domain := env.str("AWS_S3_STATIC_CUSTOM_DOMAIN", default=None):
        static_storage_options["custom_domain"] = custom_domain


STORAGES = {
    "default": {
        "BACKEND": media_storage,
        "LOCATION": private_media_location,
        "OPTIONS": default_storage_options,
    },
    "public": {
        "BACKEND": media_storage,
        "LOCATION": public_media_location,
        "OPTIONS": public_storage_options,
    },
    "staticfiles": {
        "BACKEND": static_storage,
        "LOCATION": static_static_location,
        "OPTIONS": static_storage_options,
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Global parameters

TITLE = env.str("SITE_TITLE")

if env.bool("DONATIONS_LIMIT_TO_CURRENT_YEAR"):
    DONATIONS_LIMIT_YEAR = timezone.now().year
else:
    DONATIONS_LIMIT_YEAR = env.int("DONATIONS_LIMIT_YEAR")
DONATIONS_LIMIT_MONTH = env.int("DONATIONS_LIMIT_MONTH")
DONATIONS_LIMIT_DAY = env.int("DONATIONS_LIMIT_DAY")

DONATIONS_LIMIT = datetime(
    year=DONATIONS_LIMIT_YEAR,
    month=DONATIONS_LIMIT_MONTH,
    day=DONATIONS_LIMIT_DAY,
).date()

TIMEDELTA_DONATIONS_LIMIT_DOWNLOAD_DAYS = env.int("TIMEDELTA_DONATIONS_LIMIT_DOWNLOAD_DAYS")

DONATIONS_XML_LIMIT_PER_FILE = env.int("DONATIONS_XML_LIMIT_PER_FILE")

DONATIONS_LIMIT_MONTH_NAME = [
    "Ianuarie",
    "Februarie",
    "Martie",
    "Aprilie",
    "Mai",
    "Iunie",
    "Iulie",
    "August",
    "Septembrie",
    "Octombrie",
    "Noiembrie",
    "Decembrie",
][DONATIONS_LIMIT.month - 1]

START_YEAR = 2016

LIST_OF_COUNTIES = [county[1] for county in COUNTIES_CHOICES]

FORM_COUNTIES = deepcopy(LIST_OF_COUNTIES)
try:
    FORM_COUNTIES.pop(LIST_OF_COUNTIES.index("București"))
except IndexError:
    pass

FORM_COUNTIES_NATIONAL = deepcopy(FORM_COUNTIES)
FORM_COUNTIES_NATIONAL.insert(0, "Național")

CONTACT_EMAIL_ADDRESS = env.str("CONTACT_EMAIL_ADDRESS")


# Unfold Admin settings

SIDEBAR_NAVIGATION = [
    # Supported icon set: https://fonts.google.com/icons
    {
        "title": _("Donations"),
        "items": [
            {
                "title": _("NGOs"),
                "icon": "foundation",
                "link": reverse_lazy("admin:donations_ngo_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Donations"),
                "icon": "edit_document",
                "link": reverse_lazy("admin:donations_donor_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Partners"),
                "icon": "handshake",
                "link": reverse_lazy("admin:partners_partner_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Donation exports"),
                "icon": "file_copy",
                "link": reverse_lazy("admin:donations_job_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
    {
        "title": _("Users"),
        "items": [
            {
                "title": _("Users"),
                "icon": "person",
                "link": reverse_lazy("admin:users_user_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Groups"),
                "icon": "group",
                "link": reverse_lazy("admin:users_groupproxy_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
    {
        "title": _("Django Q"),
        "items": [
            {
                "title": _("Failed tasks"),
                "icon": "assignment_late",
                "link": reverse_lazy("admin:django_q_failure_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Queued tasks"),
                "icon": "assignment_add",
                "link": reverse_lazy("admin:django_q_ormq_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Scheduled tasks"),
                "icon": "assignment",
                "link": reverse_lazy("admin:django_q_schedule_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
            {
                "title": _("Successful tasks"),
                "icon": "assignment_turned_in",
                "link": reverse_lazy("admin:django_q_success_changelist"),
                "permission": lambda request: request.user.is_superuser,
            },
        ],
    },
]

UNFOLD = {
    # https://unfoldadmin.com/docs/configuration/settings/
    # Site configuration
    "ENVIRONMENT": "redirectioneaza.callbacks.environment_callback",
    # Site customization
    "SITE_HEADER": f"Admin | {VERSION_LABEL}",
    "SITE_TITLE": TITLE,
    "SITE_ICON": lambda request: static("images/logo-smaller.png"),
    "SITE_LOGO": lambda request: static("images/logo-smaller.png"),
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "type": "image/png",
            "href": lambda request: static("images/favicon/favicon-16x16.png"),
        },
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("images/favicon/favicon-32x32.png"),
        },
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            50: "#F2C512",
            100: "#F2C617",
            200: "#F3CA25",
            300: "#F4CC2F",
            400: "#F4D03E",
            500: "#F5D449",
            600: "#F3C921",
            700: "#DAB00C",
            800: "#B3910A",
            900: "#876E07",
            950: "#745E06",
        },
    },
    # Sidebar settings
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": SIDEBAR_NAVIGATION,
    },
}


# Django Q2 — https://django-q2.readthedocs.io/en/stable/configure.html#configuration

Q_CLUSTER_WORKERS: int = env.int("DJANGO_Q_WORKERS_COUNT")
Q_CLUSTER_RECYCLE: int = env.int("DJANGO_Q_RECYCLE_RATE")
Q_CLUSTER_TIMEOUT: int = env.int("DJANGO_Q_TIMEOUT_SECONDS")
Q_CLUSTER_RETRY: int = Q_CLUSTER_TIMEOUT + (env.int("DJANGO_Q_RETRY_AFTER_TIMEOUT_SECONDS") or 1)
Q_CLUSTER_POLL: int = env.int("DJANGO_Q_POLL_SECONDS")

Q_CLUSTER = {
    "name": "redirect",
    "workers": Q_CLUSTER_WORKERS,
    "recycle": Q_CLUSTER_RECYCLE,
    "timeout": Q_CLUSTER_TIMEOUT,
    "retry": Q_CLUSTER_RETRY,
    "ack_failures": True,
    "max_attempts": 2,
    "compress": True,
    "save_limit": 200,
    "cpu_affinity": 1,
    "label": "Django Q2",
    "orm": "default",
    "poll": Q_CLUSTER_POLL,
    "guard_cycle": 3,
    "catch_up": False,
}

IMPORT_METHOD = env.str("IMPORT_METHOD")
IMPORT_USE_BATCHES = env.bool("IMPORT_USE_BATCHES")
IMPORT_BATCH_SIZE = env.int("IMPORT_BATCH_SIZE")

# reCAPTCHA & Analytics settings
GOOGLE_ANALYTICS_ID = env.str("GOOGLE_ANALYTICS_ID")

RECAPTCHA_PUBLIC_KEY = env.str("CAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env.str("CAPTCHA_PRIVATE_KEY")
RECAPTCHA_REQUIRED_SCORE = env.float("CAPTCHA_REQUIRED_SCORE")

RECAPTCHA_VERIFY_URL = env.str("CAPTCHA_VERIFY_URL")
RECAPTCHA_POST_PARAM = env.str("CAPTCHA_POST_PARAM")

RECAPTCHA_ENABLED = env.bool("RECAPTCHA_ENABLED", True if RECAPTCHA_PUBLIC_KEY else False)

if DEBUG or not RECAPTCHA_ENABLED:
    SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]


# Encryption settings
ENCRYPT_KEY = env.str("ENCRYPT_KEY", "%INVALID%")
if len(ENCRYPT_KEY) != 32 or ENCRYPT_KEY == "%INVALID%":
    raise Exception("ENCRYPT_KEY must be exactly 32 characters long")
FERNET_OBJECT = Fernet(urlsafe_b64encode(ENCRYPT_KEY.encode("utf-8")))


# Feature flags
ENABLE_FLAG_CONTACT = env.bool("ENABLE_FLAG_CONTACT", False)

# Configurations for the NGO Hub integration
UPDATE_ORGANIZATION_METHOD = env("UPDATE_ORGANIZATION_METHOD")

# Other settings
ENABLE_FULL_CUI_VALIDATION = env.bool("ENABLE_FULL_CUI_VALIDATION")

# Form download settings
ENABLE_FORMS_DOWNLOAD = env.bool("ENABLE_FORMS_DOWNLOAD", True)
TIMEDELTA_FORMS_DOWNLOAD_MINUTES = env.int("TIMEDELTA_FORMS_DOWNLOAD_MINUTES")


# Login & Auth settings
LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGOUT_REDIRECT_URL = reverse_lazy("home")

AWS_COGNITO_DOMAIN = env.str("AWS_COGNITO_DOMAIN")
AWS_COGNITO_CLIENT_ID = env.str("AWS_COGNITO_CLIENT_ID")
AWS_COGNITO_CLIENT_SECRET = env.str("AWS_COGNITO_CLIENT_SECRET")
AWS_COGNITO_USER_POOL_ID = env.str("AWS_COGNITO_USER_POOL_ID")
AWS_COGNITO_REGION = env.str("AWS_COGNITO_REGION")

# Django Allauth settings
SOCIALACCOUNT_PROVIDERS = {
    "amazon_cognito": {
        "DOMAIN": "https://" + AWS_COGNITO_DOMAIN,
        "EMAIL_AUTHENTICATION": True,  # TODO
        "VERIFIED_EMAIL": True,  # TODO
        "APPS": [
            {
                "client_id": AWS_COGNITO_CLIENT_ID,
                "secret": AWS_COGNITO_CLIENT_SECRET,
            },
        ],
    }
}

# Django Allauth Social Login adapter
SOCIALACCOUNT_ADAPTER = "redirectioneaza.social_adapters.UserOrgAdapter"

# Django Allauth allow only social logins
SOCIALACCOUNT_ONLY = False
SOCIALACCOUNT_ENABLED = True
ACCOUNT_EMAIL_VERIFICATION = "none"

# NGO Hub settings
NGOHUB_HOME_HOST = env("NGOHUB_HOME_HOST")
NGOHUB_HOME_BASE = f"https://{env('NGOHUB_HOME_HOST')}/"
NGOHUB_APP_BASE = f"https://{env('NGOHUB_APP_HOST')}/"
NGOHUB_API_HOST = env("NGOHUB_API_HOST")
NGOHUB_API_BASE = f"https://{NGOHUB_API_HOST}/"
NGOHUB_API_ACCOUNT = env("NGOHUB_API_ACCOUNT")
NGOHUB_API_KEY = env("NGOHUB_API_KEY")

# NGO Hub user roles
NGOHUB_ROLE_SUPER_ADMIN = "super-admin"
NGOHUB_ROLE_NGO_ADMIN = "admin"
NGOHUB_ROLE_NGO_EMPLOYEE = "employee"
