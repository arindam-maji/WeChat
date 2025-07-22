import os
# Set DJANGO_SETTINGS_MODULE before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
# Only now import Django modules
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack



# Import routing after setting the environment
import app1.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # initializes Django
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app1.routing.websocket_urlpatterns
        )
    ),
})