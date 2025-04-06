"""
ASGI config for cloneapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import base.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloneapp.settings')
# ProtocolTypeRouter takes a mapping of protocol type names to other Application instances, and dispatches to the right one based on protocol name (or raises an error)
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            base.routing.websocket_urlpatterns
        )
    )

})


