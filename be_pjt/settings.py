from datetime import timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='dj_rest_auth.registration.serializers')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8^^0#&-8j+rr5^ja0&g-_)v@=jt&pvufk56ie#f#q36pq@%-_m'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'accounts',
    'books',
    'chats',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    'dj_rest_auth.registration',
    'rest_framework_simplejwt.token_blacklist', 
    'django.contrib.sites',
]

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 최상단으로
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     "allauth.account.middleware.AccountMiddleware",
# ]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

SPECTACULAR_SETTINGS = {
    'COMPONENT_SPLIT_REQUEST': True,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = "none"

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY' : True,
    'JWT_AUTH_COOKIE': 'dongwha-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'dongwha-auth-refresh',
    'JWT_AUTH_COOKIE_USE_CSRF' : True,
    'JWT_AUTH_SECURE': False,
    'JWT_AUTH_SAMESITE': 'Lax',
    'SESSION_LOGIN' : False,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'REGISTER_SERIALIZER' : 'accounts.serializers.SignUpSerializer',
}

# REST_AUTH = {
#     'USE_JWT': True,
#     'JWT_AUTH_COOKIE':'accessToken',
#     # 'JWT_AUTH_REFRESH_COOKIE':'refreshToken',
#     'JWT_AUTH_HTTPONLY': False, # js 엑세스 불가
#     'JWT_AUTH_SECURE': False,   #https 만 false / 배포시에 True
#     # 'JWT_AUTH_SAMESITE': 'Strict',
#     # 'JWT_AUTH_SAMESITE': 'None',
# }


ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True 

ROOT_URLCONF = 'be_pjt.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'be_pjt.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles' 

STATICFILES_DIRS = [                    
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        # 필요시 추가 설정
    }
}