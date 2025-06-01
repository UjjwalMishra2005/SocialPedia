"""
ASGI config for cloneapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""



from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloneapp.settings')
# ProtocolTypeRouter takes a mapping of protocol type names to other Application instances, and dispatches to the right one based on protocol name (or raises an error)
from base import routing
from channels.security.websocket import AllowedHostsOriginValidator
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        ))
    )

})


