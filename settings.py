DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'test_database.sqlite3'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = 'media_root/'
MEDIA_URL = '/site_media/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'y-&_(u3odpxk%(+f*_^5bfn0nseq#jj3ef8vf3kh9-2i$zmk-v'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    'templates/',
)

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.markup',
    'forum',
    'userprofile',
    'news',
    'staticpages',
)


AUTH_PROFILE_MODULE = 'userprofile.userprofile'


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media"
)

APPEND_SLASH = False

FORUM_MAX_DAY_MARK = 10
