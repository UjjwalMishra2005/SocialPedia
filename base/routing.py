from django.urls import path
from base.consumers import *
websocket_urlpatterns=[
    path('ws/socket-server/<chatroom_name>', BaseConsumer.as_asgi())
]