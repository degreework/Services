"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

####################
#site settings
SITE_URL='http://127.0.0.1:8080/'
SITE_NAME='Back-end'

#client site settings
SITE_CLIENT_URL = "http://127.0.0.1:8000"
SITE_CLIENT_NAME = "Front-end"
SITE_CLIENT_URL_CONFIRM_PASSWORD_RECOVERY = SITE_CLIENT_URL + "/password/reset/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))
SECRET_KEY = '-8_@1g4*^8efmhj^rc!j(&o@=zd5_^4^5y_(^zwa@9l4uxx+i6'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG', True)
DEBUG = True

#ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sessions.backends.signed_cookies',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #3
    'waliki',
    'waliki.git',
    'waliki.rest',

    #3 parties
    'rest_framework',


    #Oauth
    'oauth2_provider',
    #'rest_framework',

    #cross-origin
    'corsheaders',

    #for create thumbnails and optimize uploaded images
    'easy_thumbnails', 
    'easy_thumbnails.optimize',

    'post_framework',
    'forum',
    'comment',
    
    
    'material',
    'wiki',

    #Evaluations
    'quiz',
    'multichoice',
    'true_false',
    'essay',
    'servicio',

    #Activities
    'activitie',

    #gamification
    'gamification',
    'badger',

    #user' wall
    'actstream',


    #
    'notifications',
    'reminder',

    'module',


   #App REST for Users
    'users',
    'degree',
    
)

"""
if DEBUG:
    INSTALLED_APPS += ('django_extensions', )
"""

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'waliki.rest.middleware.CoffeehouseMiddleware',


)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', os.path.join(BASE_DIR, 'users', 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

#setting model for login
AUTH_USER_MODEL = 'users.User'


DEFAULT_GROUP_NAME = {
    "Registered": (
        "users | user | Can view Users",
        "users | user | Can change user",

        "waliki | Page | Can add Page",
        "waliki | Page | Can view page",

        "forum | Ask | Can view Asks",
        "forum | Ask | Can add Ask",
        "forum | Ask | Can change Ask",

        "module | Module | Can view Module",

        ),
    "Teacher":(
        "activitie | ActivitieParent | Can add ActivitieParent",
        "activitie | ActivitieParent | Can change ActivitieParent",
        "activitie | ActivitieParent | Can delete ActivitieParent",

        "activitie | ActivitieChild | Can check activities",

        "module | Module | Can add Module",
        )
    }

REGISTRATION_DEFAULT_GROUP_NAME = ("Registered", )


OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'EDIT_PROFILE': 'Editar perfil', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #temp
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        #end
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        ),
    }

# Cross-origin
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ('http://127.0.0.1:8000', )


MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')
MEDIA_URL = "/media/"


STATIC_ROOT = os.path.join(BASE_DIR, 'STATICS/')


#settings for thumbnails
#THUMBNAIL_BASEDIR = 'thum'
#THUMBNAIL_EXTENSION = 'jpg'
#THUMBNAIL_NAMER = 'easy_thumbnails.namers.hashed'

#sizes for images
THUMBNAIL_ALIASES = {
    '': {
        'mini': {'size': (50, 50), 'crop': True},
        'user_profile': {'size': (168, 168), 'crop': True},
        'module_image': {'size': (200, 200), 'crop': True},
    },
}

DEFAULT_USER_IMAGE_SETTING = THUMBNAIL_ALIASES['']['user_profile']
DEFAULT_MODULE_IMAGE_SETTING = THUMBNAIL_ALIASES['']['module_image']



#waliki
#Walikis content path. By default its <project_root>/waliki_data
#WALIKI_DATA_DIR = <path>

#The slug of the index page
#WALIKI_INDEX_SLUG = 'index'

#WALIKI_COMMITTER_EMAIL = email@alg
#WALIKI_COMMITTER_NAME = name

WALIKI_API_ROOT = 'v0'

WALIKI_LOGGED_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')
WALIKI_ANONYMOUS_USER_PERMISSIONS = ( 'view_page', )


WALIKI_PAGINATE_BY = 5
WALIKI_AVAILABE_MARKUPS = ['Markdown']

#########################
#slumber
"""
SLUMBER_DIRECTORY = {
    'users': 'users',
    'post_framework': 'post_framework',
}
SLUMBER_SERVICE = 'users'
SLUMBER_CLIENT_APPS = ['post_framework']
"""


######################
# Email settings

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'knowahora@gmail.com'
EMAIL_HOST_PASSWORD = 'Gp4ssm41L'


########################
# Badge default 
DEFAULT_BADGE_SETTING = {'title':'titulo' , 'slug':'slug', 'description':'description', 'image':'', 'unique':True ,'nominations_accepted':False, 'nominations_autoapproved':False, 'points_end': 50}



#########################
# notifications

NOTIFICATIONS = True

#########################
# Stream (User's wall)

ACTSTREAM_SETTINGS = {
    #'MANAGER': 'myapp.managers.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': False,
    'GFK_FETCH_DEPTH': 1,
}