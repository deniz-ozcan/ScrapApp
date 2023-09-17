from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-8&q=0w)6@o&19n_pqr(uf*n(b$=lk*_0dye7oukba24gbip8=r"
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'scrap',
    'shop',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
CRISPY_CLASS_CONVERTERS = {
    'textinput': "form-control cst__radius",
    'urlinput': "form-control cst__radius",
    'numberinput': "form-control cst__radius",
    'emailinput': "form-control cst__radius",
    'dateinput': "form-control cst__radius",
    'textarea': "form-control cst__radius",
    'passwordinput': "form-control cst__radius",
    'select': "form-select form-select-sm",
    'checkboxinput': "form-check-input",
    
}
ROOT_URLCONF = "scrapapp.urls"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            BASE_DIR / "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
