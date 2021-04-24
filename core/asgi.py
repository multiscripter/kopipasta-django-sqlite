"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os, sys

# Эти пути необходимы для работы на бое в режиме mod_wsgi как демона.
# Решают проблему ModuleNotFoundError: No module named 'имя_модуля'
sys.path.append('/home/cyberbotx/.local/lib/python3.8/site-packages')
sys.path.append('/var/www/kopipasta-django-sqlite')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.asgi import get_asgi_application

kopipasta_app = get_asgi_application()
