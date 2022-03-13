import os

from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'l+57pdz1&9n(18h0vnm+pfjwd8nw(9r6$7_gtd2=+(s6tst8rc'
)


include(
    'components/database.py',
    'components/config.py',
)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'api',
    'users',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_FILTER_BACKENDS':
        ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100000/day',
        'anon': '10000/day',
        'low_request': '300/minute',
    }
}


DJOSER = {
    'SET_PASSWORD_RETYPE ': True,
    'HIDE_USERS': False,
    'SERIALIZERS': {
            'user_create': 'users.serializers.UserSerializer',
            'current_user': 'users.serializers.UserSerializer',
            'user': 'users.serializers.UserSerializer',
    },
    'PERMISSIONS': {
            "activation": ["rest_framework.permissions.AllowAny"],
            "password_reset": ["rest_framework.permissions.AllowAny"],
            "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
            "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
            "username_reset": ["rest_framework.permissions.IsAdminUser"],
            "username_reset_confirm": [
                "rest_framework.permissions.IsAdminUser"
            ],
            "set_username": ["djoser.permissions.IsAdminUser"],
            "user_create": ["rest_framework.permissions.AllowAny"],
            "user_delete": ["djoser.permissions.IsAdminUser"],
            "user": ["rest_framework.permissions.AllowAny"],
            "user_list": ["rest_framework.permissions.AllowAny"],
            "token_create": ["rest_framework.permissions.AllowAny"],
            "token_destroy": ["djoser.permissions.CurrentUserOrAdmin"],
        }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


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
