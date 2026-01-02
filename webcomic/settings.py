# Reload triggered for URL debug
from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-6j=2a07g#m8qi4xywd*e!o&v(n4ve#i_h%u6uxaywyt-ka_w!$')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'surchaing.edmateo.site', '.render.com', '.onrender.com']

CSRF_TRUSTED_ORIGINS = ['https://*.render.com', 'https://*.onrender.com', 'https://surchaing.edmateo.site']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Añadido para estáticos
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'webcomics',
    'ckeditor_uploader',  
    'perfil',
    'cloudinary_storage',
    'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Añadido para estáticos en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webcomic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webcomics.context_processors.manga_filters', 
            ],
        },
    },
]

WSGI_APPLICATION = 'webcomic.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

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

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Modern Django Storage Configuration (Required for Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'webcomics/static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Render / Production Configuration
# Trust the X-Forwarded-Proto header for SSL (Required for Render)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False # Set to True if you want to force SSL, but Render handles this usually. Safe to leave False to avoid loops if misconfigured.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Hugging Face API Configuration
# Hardcoded to resolve ZeroGPU Quota issues on Render (Validated)
HUGGINGFACE_API_TOKEN = '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'
HUGGINGFACE_DEPTH_MODEL = 'LiheYoung/depth-anything-large-hf'
HUGGINGFACE_API_URL = f'https://router.huggingface.co/hf-inference/models/{HUGGINGFACE_DEPTH_MODEL}'

# Cloudinary Storage Configuration
# Hardcoded to ensure it works on Render without Env conflicts
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dfdrbs1gp',
    'API_KEY': '688516932845499',
    'API_SECRET': '3txYI7sSbcyqDAf4SVdjlEfIe9s',
}

# Add standard Cloudinary config to force HTTPS
import cloudinary
cloudinary.config(
    cloud_name = 'dfdrbs1gp',
    api_key = '688516932845499',
    api_secret = '3txYI7sSbcyqDAf4SVdjlEfIe9s',
    secure = True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
