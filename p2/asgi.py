import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p2.settings')
django.setup()  # ✅ setup pehle karo

# ✅ Ab yahan baad mein sab import karo
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from app.routing import urls_fetch

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            urls_fetch
        )
    )
})
