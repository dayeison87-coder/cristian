from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import usuarios.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        usuarios.routing.websocket_urlpatterns
    ),
})