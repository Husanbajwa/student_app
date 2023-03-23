
import os
import appbase.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter , URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybuzz.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            appbase.routing.websocket_urlpatterns
        )
    )
})
