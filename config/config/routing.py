from django.urls import path, re_path

from config.api.consumers import RoomConsumer


websocket_urlpatterns = [
    path("ws/", RoomConsumer.as_asgi()),
    # path('ws/chat/', consumers.RoomConsumer.as_asgi()),
]