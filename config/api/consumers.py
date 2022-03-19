import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from .models import Room, Listener
from .serializers import RoomSerializer


class RoomConsumer(ObserverModelInstanceMixin,
                   GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = []
    lookup_field = "pk"


    @action()
    def add_listener_into_room(self, pk, listener_pk):
        listener = get_object_or_404(Listener, id=listener_pk)
        room = get_object_or_404(Room, id=pk)
        room.guests.add(listener)


# class RoomConsumer(
#         mixins.ListModelMixin,
#         GenericAsyncAPIConsumer,
# ):
#     permission_classes = []
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#
#     @database_sync_to_async
#     def get_room(self, pk: int) -> Room:
#         return get_object_or_404(Room, id=pk)