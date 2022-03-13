from django.contrib import admin

from .models import Listener, Sync, Room


@admin.register(Listener)
class ListenerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


@admin.register(Sync)
class SyncAdmin(admin.ModelAdmin):
    filter_horizontal = ('guests',)
    list_display = ('id', 'track_id')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('guests', 'sync')
    list_display = ('id', 'name', 'creator', 'rules', 'playlist_id')
