"""
Django settings for bookstore_project project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / 'Germaneya.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-m7!0!z4926bqo##gdx-k*g6i%4ebl6y(l4+w6&!3^$=uqo^+&-')

# SECURITY WARNING: don't run with debug turned on in production!
# Render provides a RENDER environment variable.
IS_RENDER = 'RENDER' in os.environ

if IS_RENDER:
    DEBUG = False
else:
    DEBUG = True # Keep DEBUG=True for local development

if IS_RENDER:
    # Get the Render external hostname, and also add the internal one
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]
else:
    # Allow all hosts for local development
    ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'bookstore',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps for deployment
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise middleware should be placed right after the security middleware
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookstore_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bookstore.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# This is the URL that your HTML will use to refer to static files
STATIC_URL = 'static/'

# This is the folder where 'collectstatic' will place all static files.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Define the order in which Django finds static files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# These are the folders where Django will look for static files in addition
# to each app's 'static/' directory.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

# Production settings: This block will be active ONLY when deployed on Render
if IS_RENDER:
    STORAGES = {
        # Media file storage (user uploads like book covers)
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"
        },
        # Static file storage (your app's CSS, JS, admin files)
        "staticfiles": {
            "BACKEND": "bookstore.storages.CustomStaticHashedCloudinaryStorage"
        },
    }
else:
    # Use Cloudinary for local development as well to mimic production.
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"
        },
        "staticfiles": {
            "BACKEND": "bookstore.storages.CustomStaticHashedCloudinaryStorage"
        },
    }

# Cloudinary settings
CLOUDINARY_STORAGE = {
    'EXCLUDE_DIRS': [],
}
# Make sure to set your CLOUDINARY_URL in your .env file
# It should look like: CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME

# Set the default file storage to Cloudinary

# Media files (User uploaded content)
# These are now served from Cloudinary, so local MEDIA_URL and MEDIA_ROOT are less important
# but still good practice to have for local development if not using Cloudinary locally.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Jazzmin settings
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Ismail's Bookstore Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Bookstore",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Admin",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/cover.jpg",

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Bookstore Admin Panel",

    # Copyright on the footer
    "copyright": "Isma3il's Bookstore Ltd",

    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "bookstore.Book",

    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "bookstore.Book"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "bookstore"},
    ],

     "icons": {
        "bookstore": "fas fa-book-open",
        "bookstore.book": "fas fa-book",
        "bookstore.category": "fas fa-tags",
        "bookstore.bookimage": "fas fa-image",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Cart Session ID
CART_SESSION_ID = 'cart'
