from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Listener
from .serializers import ListenerSerializer


class ListenerViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    serializer_class = ListenerSerializer
    queryset = Listener.objects.all()
