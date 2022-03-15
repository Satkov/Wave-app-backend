from rest_framework import serializers

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
        try:
            guest_ids = request_data.get('guests')
            guest_ids = guest_ids.split(', ')
            for id in guest_ids:
                int(id)
        except ValueError:
            raise serializers.ValidationError({
                'errors': 'ID пользователей должны быть числом и идти через запятую'
            })
        except AttributeError:
            pass

        try:
            sync_ids = request_data.get('sync')
            sync_ids = sync_ids.split(', ')
            for id in sync_ids:
                int(id)
        except ValueError:
            raise serializers.ValidationError({
                'errors': 'ID sync должны быть числом и идти через запятую'
            })
        except AttributeError:
            pass

        try:
            creator_id = request_data.get('creator')
            int(creator_id)
        except ValueError:
            raise serializers.ValidationError({
                'errors': 'ID создателя комнаты должны быть числом'
            })
        return data

    def create(self, validated_data):
        request_data = get_request(self.context).data
        creator = Listener.objects.get(id=request_data.get('creator'))
        room = Room.objects.create(
            name=validated_data['name'],
            creator=creator,
            rules=validated_data['rules'],
            playlist_id=validated_data['playlist_id'],
        )
        guests_ids = request_data.get('guests')
        try:
            guests = []
            for id in guests_ids.split(', '):
                guest = Listener.objects.get(id=id)
                guests.append(guest)
            room.guests.set(guests)
        except AttributeError:
            pass

        sync_ids = request_data.get('sync')
        try:
            syncs = []
            for id in sync_ids.split(', '):
                sync = Sync.objects.get(id=id)
                syncs.append(sync)
            room.sync.set(syncs)
        except AttributeError:
            pass

        return room

    def update(self, instance, validated_data):
        request_data = get_request(self.context).data
        super().update(instance, validated_data)

        guests_ids = request_data.get('guests')
        try:
            guests = []
            for id in guests_ids.split(', '):
                guest = Listener.objects.get(id=id)
                guests.append(guest)
            instance.guests.set(guests)
        except AttributeError:
            pass

        sync_ids = request_data.get('sync')
        try:
            syncs = []
            for id in sync_ids.split(', '):
                sync = Sync.objects.get(id=id)
                syncs.append(sync)
            instance.sync.set(syncs)
        except AttributeError:
            pass

        return instance

    def get_guests(self, obj):
        guests = obj.guests.all()
        serializer = ListenerSerializer(guests, many=True)
        return serializer.data

    def get_sync(self, obj):
        sync = obj.sync.all()
        serializer = SyncSerializer(sync, many=True)
        return serializer.data
