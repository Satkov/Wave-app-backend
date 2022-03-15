from rest_framework import mixins
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import GenericViewSet

from .models import Listener, Room, Sync
from .serializers import ListenerSerializer, RoomSerializer, SyncSerializer


class ListenerViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    serializer_class = ListenerSerializer
    queryset = Listener.objects.all()


class RoomViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class SyncViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = SyncSerializer
    queryset = Sync.objects.all()
