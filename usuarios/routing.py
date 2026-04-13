from django.urls import path
from .consumers import BarberoConsumer

websocket_urlpatterns = [
    path("ws/barbero/", BarberoConsumer.as_asgi()),
]