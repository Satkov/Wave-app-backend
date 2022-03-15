from django.shortcuts import get_object_or_404
from rest_framework import serializers
import json

from .models import Listener, Room, Sync
from .utils import get_request


class ListenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listener
        fields = ('id', 'username', 'email')


class SyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sync
        fields = ('track_id', 'guests')


class RoomSerializer(serializers.ModelSerializer):
    creator = ListenerSerializer(many=False, read_only=True)
    guests = serializers.SerializerMethodField()
    sync = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'creator', 'guests', 'rules',
                  'playlist_id', 'sync')

    def validate(self, data):
        request_data = get_request(self.context).data
        if request_data.get('guests'):
            try:
                guests_ids = request_data.get('guests')
                guests_ids = json.loads(guests_ids)
                for id in guests_ids:
                    int(id)
            except ValueError:
                raise serializers.ValidationError({
                    'errors': 'ID must be int'
                })

        if request_data.get('sync'):
            try:
                sync_ids = request_data.get('sync')
                sync_ids = json.loads(sync_ids)
                for id in sync_ids:
                    int(id)
            except ValueError:
                raise serializers.ValidationError({
                    'errors': 'ID sync must be int'
                })

        try:
            creator_id = request_data.get('creator')
            creator_id = json.loads(creator_id)
            int(creator_id)
        except ValueError:
            raise serializers.ValidationError({
                'errors': 'ID creator must be int'
            })

        return data

    def create(self, validated_data):
        request_data = get_request(self.context).data
        creator_id = request_data.get('creator')
        creator_id = json.loads(creator_id)
        creator = get_object_or_404(Listener, id=creator_id)
        room = Room.objects.create(
            name=validated_data['name'],
            creator=creator,
            rules=validated_data['rules'],
            playlist_id=validated_data['playlist_id'],
        )
        guests_ids = request_data.get('guests')
        if guests_ids:
            guests_ids = json.loads(guests_ids)
            guests = []
            for id in guests_ids:
                guest = get_object_or_404(Listener, id=id)
                guests.append(guest)
            room.guests.set(guests)

        sync_ids = request_data.get('sync')
        if sync_ids:
            sync_ids = json.loads(sync_ids)
            syncs = []
            for id in sync_ids:
                sync = Sync.objects.get(id=id)
                syncs.append(sync)
            room.sync.set(syncs)

        return room

    def update(self, instance, validated_data):
        request_data = get_request(self.context).data
        super().update(instance, validated_data)

        guests_ids = request_data.get('guests')
        if guests_ids:
            guests_ids = json.loads(guests_ids)
            guests = []
            for id in guests_ids:
                guest = get_object_or_404(Listener, id=id)
                guests.append(guest)
            instance.guests.set(guests)

        sync_ids = request_data.get('sync')
        if sync_ids:
            sync_ids = json.loads(sync_ids)
            syncs = []
            for id in sync_ids:
                sync = Sync.objects.get(id=id)
                syncs.append(sync)
            instance.sync.set(syncs)

        return instance

    def get_guests(self, obj):
        guests = obj.guests.all()
        serializer = ListenerSerializer(guests, many=True)
        return serializer.data

    def get_sync(self, obj):
        sync = obj.sync.all()
        serializer = SyncSerializer(sync, many=True)
        return serializer.data
