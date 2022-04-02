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
from .serializers import RoomSerializer, ListenerSerializer


class RoomConsumer(ObserverModelInstanceMixin,
                   GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = []
    lookup_field = "pk_user"


    @action()
    async def join_room(self, pk_user, pk_room, **kwargs):
        self.channel_layer.group_add("room", self.channel_name)
        print(self.channel_name)
        self.room_subscribe = pk_room
        await self.add_user_to_room(pk_user)
        print("2--------------")
        await self.notify_users()

    @database_sync_to_async
    def add_user_to_room(self, pk_user):
        listener = get_object_or_404(Listener, id=pk_user)
        if not listener.current_rooms.filter(pk=self.room_subscribe).exists():
            listener.current_rooms.add(get_object_or_404(Room, id=self.room_subscribe))

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        print("3--------------", self.groups)
        await self.channel_layer.group_send(
            'room',
            {
                'type': 'update_users',
                'usuarios': await self.current_users(room)
            }
        )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def current_users(self, room: Room):
        return [ListenerSerializer(guest).data for guest in room.guests.all()]

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return get_object_or_404(Room, id=pk)

