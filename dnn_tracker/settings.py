"""
Django settings for dnn_tracker project.
Firebase Firestore + Vercel serverless.
"""
import os
import json
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')
_allowed = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,.vercel.app').strip()
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]
# Always allow Vercel deployment URLs (preview and production)
if '.vercel.app' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.vercel.app')

# Application definition
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'tracker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dnn_tracker.urls'
WSGI_APPLICATION = 'dnn_tracker.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'tracker.context_processors.streak',
            ],
        },
    },
]

# Static files (Vercel)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Local .env first (so Firebase can be set there)
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

# Firebase: load from file path OR from env JSON string
FIREBASE_CREDENTIALS = None
_creds_path = os.environ.get('FIREBASE_CREDENTIALS_PATH')
if _creds_path:
    _path = Path(_creds_path)
    if not _path.is_absolute():
        _path = BASE_DIR / _path
    if _path.exists():
        try:
            with open(_path, 'r') as f:
                FIREBASE_CREDENTIALS = json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
if not FIREBASE_CREDENTIALS:
    _creds_json = os.environ.get('FIREBASE_CREDENTIALS')
    if _creds_json:
        try:
            FIREBASE_CREDENTIALS = json.loads(_creds_json)
        except json.JSONDecodeError:
            pass

# Default primary key (minimal Django)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# No database (Firestore only)
DATABASES = {}
