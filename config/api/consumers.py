import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from .models import Room, Listener
from .serializers import RoomSerializer, ListenerSerializer

class RoomConsumer(ObserverModelInstanceMixin,
                   GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = []
    lookup_field = "pk"

    @action()
    async def subscribe_to_room_guests(self, pk, **kwargs):
        await self.room_guests.subscribe(room=pk)

    @model_observer(Room)
    async def room_guests(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @room_guests.groups_for_signal
    def room_guests(self, instance: Room, **kwargs):
        yield f'pk__{instance.pk}'

    @room_guests.groups_for_consumer
    def room_guests(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @room_guests.serializer
    def room_guests(self, instance: Room, action, **kwargs):
        return dict(data=RoomSerializer(instance).data, action=action.value, pk=instance.pk)
