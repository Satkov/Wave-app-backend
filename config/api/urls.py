
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListenerViewSet, RoomViewSet, SyncViewSet

router = DefaultRouter()

router.register(r'listener', ListenerViewSet, basename='Listener')
router.register(r'room', RoomViewSet, basename='RoomViewSet')
router.register(r'sync', SyncViewSet, basename='Sync')


urlpatterns = [
    path('', include(router.urls)),
]