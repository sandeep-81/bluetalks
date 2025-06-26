from django.urls import path
from .consumer import MySyncConsumer , RandomChatSync , LoginChatConsumer
urls_fetch = [
    path('ws/sc/chat/<str:group_no>/',MySyncConsumer.as_asgi()),
    path('ws/sc/randchat/',RandomChatSync.as_asgi()), 
    path('ws/sc/user/<str:friend_username>/',LoginChatConsumer.as_asgi()), 
]
  