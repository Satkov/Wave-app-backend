
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListenerViewSet, RoomViewSet, SyncViewSet, GetUsersRooms

router = DefaultRouter()

router.register(r'listener', ListenerViewSet, basename='Listener')
router.register(r'room', RoomViewSet, basename='RoomViewSet')
router.register(r'sync', SyncViewSet, basename='Sync')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/get_users_rooms', GetUsersRooms.as_view(), name='get_users_rooms')
]