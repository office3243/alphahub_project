import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '+qkf6u0n7@xpqt#0_c61pmacz)tk%rgv*65m!-mrb%5s8#ga_c'

DEBUG = True

ALLOWED_HOSTS = ["*", ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "accounts",
    "orders",
    "products",
    "portal",
    "carts_app",
    "django_filters",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alphahub_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'alphahub_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

#   CUSTOM SETTINGS
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"
SITE_DOMAIN_NAKED = "http://127.0.0.1:8000"


#   PAYTM
PAYTM_MERCHANT_KEY = "xt94GuDiIMz_#84O"
PAYTM_MERCHANT_ID = "ZIHCDc43188965988448"
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CALLBACK_URL = SITE_DOMAIN_NAKED + "/payments/paytm/response/"


API_KEY_2FA = "c9ef2a2e-806a-11e9-ade6-0200cd936042"
