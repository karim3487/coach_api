"""WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from decouple import config
from django.core.wsgi import get_wsgi_application

env = config("ENV", default="dev")
valid_envs = {"dev", "prod"}

if env not in valid_envs:
    raise ValueError(f"Invalid DJANGO_ENV: {env}. Choose from {valid_envs}")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{env}")

application = get_wsgi_application()
