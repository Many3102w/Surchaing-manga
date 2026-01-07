"""
WSGI config for webcomic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')

application = get_wsgi_application()

# Start the keep-alive bot
try:
    from .keep_alive import start_keep_alive
    start_keep_alive()
except ImportError:
    pass
