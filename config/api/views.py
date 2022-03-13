# from rest_framework import mixins
# from rest_framework.viewsets import GenericViewSet
#
# from .serializers import ListenerSerializer
#
#
# class TagViewSet(mixins.RetrieveModelMixin,
#                  mixins.ListModelMixin,
#                  GenericViewSet):
#     serializer_class = ListenerSerializer
#     queryset = Tag.objects.all()
#     pagination_class = None