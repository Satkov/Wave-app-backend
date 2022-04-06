from django.shortcuts import get_object_or_404
from djangochannelsrestframework.decorators import action
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Listener, Room, Sync
from .serializers import ListenerSerializer, RoomSerializer, SyncSerializer


class ListenerViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    serializer_class = ListenerSerializer
    queryset = Listener.objects.all()


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class SyncViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = SyncSerializer
    queryset = Sync.objects.all()


class GetUsersRooms(APIView):
    def get(self, request):
        try:
            user_id = request.data['user_id']
        except KeyError:
            raise ValidationError({'error': 'user_id is required'})
        listener = get_object_or_404(Listener, id=user_id)
        rooms = Room.objects.filter(guests=listener)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)