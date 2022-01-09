from django.urls import re_path, path

from celerydemo import consumers

ws_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]