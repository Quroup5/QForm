from .settings import *

DEBUG = env.bool('DJANGO_DEBUG', default=True)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("PG_NAME"),
        'USER': env.str("PG_USER"),
        'PASSWORD': env.str("PG_PASSWORD"),
        'HOST': env.str("PG_HOST"),
        'PORT': env.str("PG_PORT"),
    }
}
