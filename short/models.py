from django.db import models
from django.contrib.auth.models import User


class NativeLink(models.Model):
    nativelink = models.CharField(max_length=32, db_index=True)


class Link(models.Model):
    nativelink = models.ForeignKey(NativeLink, on_delete=models.CASCADE, db_index=True)
    short_link = models.CharField(max_length=32, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    follow = models.IntegerField(default=0)


class Key(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    data = models.CharField(max_length=512, unique=True)
    expire_time = models.DateTimeField()
