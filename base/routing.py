from django.urls import path
from base.consumers import BaseConsumer
websocket_urlpatterns=[
    path('ws/socket-server/<chatroom_name>', BaseConsumer.as_asgi())
]