import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import usuarios.routing  # <--- Reemplaza 'usuarios' por el nombre real de tu app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firebase.settings') # <--- Tu nombre de proyecto

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            usuarios.routing.websocket_urlpatterns
        )
    ),
})