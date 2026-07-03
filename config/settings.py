from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep secret in production!
SECRET_KEY = os.getenv("SECRET_KEY", "temporary-build-key-not-used-in-production")

# SECURITY WARNING: never run with DEBUG=True in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

# Locally: 127.0.0.1 — on Railway: your-app.railway.app
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# --- Apps ---

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",

    # Third-party apps
    "captcha",
    "robots",

    # Local apps
    "apps.accounts.apps.AccountsConfig",
    "apps.core.apps.CoreConfig",
    "apps.blog.apps.BlogConfig",
]

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Default site used by Django's Sites Framework.
SITE_ID = 1

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.google_maps_key",
            ],
        },
    },
]

# Entry point used by WSGI servers (e.g. Gunicorn) to serve this Django application.
WSGI_APPLICATION = "config.wsgi.application"

# --- Database ---
# Database configuration (SQLite for development, DATABASE_URL for production)
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization & Timezone ---
LANGUAGE_CODE = "en-us"       # Default language for Django and admin
TIME_ZONE = "Asia/Tehran"     # Default project timezone
USE_I18N = True               # Enable Django's translation framework
USE_TZ = True                 # Use timezone-aware datetimes

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# User uploaded files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Trusted origins allowed to send CSRF-protected requests (configured via environment variables).
CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin
]



# URL to redirect users when they are NOT authenticated
LOGIN_URL = "accounts:login"
# URL to redirect users AFTER successful login
LOGIN_REDIRECT_URL = "core:home"
# URL to redirect users AFTER logout
LOGOUT_REDIRECT_URL = "core:home"


# -------------------------------------------------------------------
# Media Storage (Production Only)
# -------------------------------------------------------------------
# During development (DEBUG=True):
#   - Static files are served locally.
#   - Uploaded media files are stored inside MEDIA_ROOT.
#
# During production (DEBUG=False):
#   - Uploaded media files are stored in Supabase Storage (S3 API).
#   - Static files are served by WhiteNoise.
# -------------------------------------------------------------------

if not DEBUG:

    # Configure Django's storage backends.
    STORAGES = {
        # Default storage backend (user uploaded files).
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        },

        # Static files storage.
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }

    # ----------------------------------------------------------------
    # Supabase Storage Credentials
    # ----------------------------------------------------------------
    # These values are loaded from environment variables to keep
    # secrets out of the source code.
    AWS_ACCESS_KEY_ID = os.getenv("SUPABASE_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("SUPABASE_SECRET_KEY")

    # ----------------------------------------------------------------
    # Storage Bucket
    # ----------------------------------------------------------------
    # Name of the bucket where uploaded media files are stored.
    AWS_STORAGE_BUCKET_NAME = "media"

    # ----------------------------------------------------------------
    # Supabase S3 Endpoint
    # ----------------------------------------------------------------
    # Django communicates with Supabase using its S3-compatible API.
    AWS_S3_ENDPOINT_URL = os.getenv("SUPABASE_S3_ENDPOINT")

    # ----------------------------------------------------------------
    # Storage Behaviour
    # ----------------------------------------------------------------

    # Prevent uploaded files with the same name from overwriting
    # existing files.
    AWS_S3_FILE_OVERWRITE = False

    # Make uploaded files publicly accessible.
    AWS_DEFAULT_ACL = "public-read"

    # Generate clean public URLs without temporary signed query strings.
    AWS_QUERYSTRING_AUTH = False

    # S3 region used by the storage backend.
    AWS_S3_REGION_NAME = os.getenv("SUPABASE_REGION", "us-east-1")

    # Signature version used when communicating with the S3 API.
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    # Public base URL used to access uploaded media files.
    AWS_S3_CUSTOM_DOMAIN = (
        f"{os.getenv('SUPABASE_PROJECT_ID')}"
        ".supabase.co/storage/v1/object/public/media"
    )