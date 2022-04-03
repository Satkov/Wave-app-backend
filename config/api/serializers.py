from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Listener, Room, Sync
from .utils import get_request


class ListenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listener
        fields = ('display_name', 'id')


class SyncSerializer(serializers.ModelSerializer):
    guests = serializers.SerializerMethodField()

    class Meta:
        model = Sync
        fields = ('id', 'track_id', 'guests')

    def validate(self, data):
        request_data = get_request(self.context).data

        try:
            guests_ids = request_data.get('guests')
            for id in guests_ids:
                int(id)
        except ValueError:
            raise serializers.ValidationError({
                'errors': 'ID must be int'
            })
        return data

    def create(self, validated_data):
        request_data = get_request(self.context).data
        sync = Sync.objects.create(
            track_id=validated_data['track_id']
        )
        guests_ids = request_data.get('guests')
        guests = []
        for id in guests_ids:
            guest = get_object_or_404(Listener, id=id)
            guests.append(guest)
        sync.guests.set(guests)
        return sync

    def update(self, instance, validated_data):
        request_data = get_request(self.context).data
        super().update(instance, validated_data)
        guests_ids = request_data.get('guests')
        guests = []
        for id in guests_ids:
            guest = get_object_or_404(Listener, id=id)
            guests.append(guest)
        instance.guests.set(guests)
        return instance

    def get_guests(self, obj):
        guests = obj.guests.all()
        serializer = ListenerSerializer(guests, many=True)
        return serializer.data


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
        guests_ids = request_data.get('guests')
        creator_id = request_data.get('creator')

        try:
            Listener.objects.get(id=creator_id)
        except Listener.DoesNotExist:
            raise serializers.ValidationError({
                'errors': 'This creator does not exists'
            })

        try:
            for id in guests_ids:
                Listener.objects.get(id=id)
        except Listener.DoesNotExist:
            raise serializers.ValidationError({
                'errors': 'Some guest does not exist'
            })
        except TypeError:
            pass

        try:
            sync_ids = request_data.get('sync')
            for id in sync_ids:
                int(id)
        except ValueError:
            raise serializers.ValidationError({
                'errors': 'ID sync must be int'
            })
        except TypeError:
            pass

        return data

    def create(self, validated_data):
        request_data = get_request(self.context).data
        creator_id = request_data.get('creator')
        creator = get_object_or_404(Listener, id=creator_id)
        room = Room.objects.create(
            name=validated_data['name'],
            creator=creator,
            playlist_id=validated_data['playlist_id'],
        )
        try:
            room.rules = validated_data['rules']
        except KeyError:
            pass
        guests_ids = request_data.get('guests')
        try:
            guests = []
            for id in guests_ids:
                guest = get_object_or_404(Listener, id=id)
                guests.append(guest)
            room.guests.set(guests)
        except TypeError:
            pass

        sync_ids = request_data.get('sync')
        try:
            syncs = []
            for id in sync_ids:
                sync = Sync.objects.get(id=id)
                syncs.append(sync)
            room.sync.set(syncs)
        except TypeError:
            pass

        return room

    def update(self, instance, validated_data):
        request_data = get_request(self.context).data
        super().update(instance, validated_data)

        guests_ids = request_data.get('guests')
        try:
            guests = []
            for id in guests_ids:
                guest = get_object_or_404(Listener, id=id)
                guests.append(guest)
            instance.guests.set(guests)
        except TypeError:
            pass

        sync_ids = request_data.get('sync')
        try:
            syncs = []
            for id in sync_ids:
                sync = get_object_or_404(Sync, id=id)
                syncs.append(sync)
            instance.sync.set(syncs)
        except TypeError:
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
