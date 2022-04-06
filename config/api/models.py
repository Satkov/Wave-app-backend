import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Listener(models.Model):
    index = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(_('display_name'), max_length=300)
    id = models.CharField(_('id'), max_length=300)

    class Meta:
        verbose_name = _('listener')
        verbose_name_plural = _('listener')
        indexes = [models.Index(fields=['display_name'], name='lister_display_name_idx')]

    def __str__(self):
        return self.display_name


class Sync(models.Model):
    track_id = models.CharField(max_length=254, null=False)
    guests = models.ManyToManyField(Listener)


class Room(models.Model):
    name = models.CharField(_('channel name'), max_length=50)
    creator = models.ForeignKey(Listener, related_name='Creator', null=False, on_delete=models.CASCADE)
    guests = models.ManyToManyField(Listener)
    rules = models.TextField(_('rules'), null=True, blank=True)
    playlist_id = models.CharField(_('playlist id'), null=False, max_length=254)
    sync = models.ManyToManyField(Sync, blank=True)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('room')

    def __str__(self):
        return self.name
