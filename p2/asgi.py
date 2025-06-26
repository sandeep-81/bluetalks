
import os
from channels.routing import ProtocolTypeRouter,URLRouter
from app.routing import urls_fetch 
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p2.settings')


application = ProtocolTypeRouter({
   'http': get_asgi_application(),
   'websocket': AuthMiddlewareStack(URLRouter(
       urls_fetch
   ))
   } )
