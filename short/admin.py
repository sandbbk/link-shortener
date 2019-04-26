from django.contrib import admin
from .models import (Link, NativeLink)


class LinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Link._meta.fields]


class NativeLinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NativeLink._meta.fields]


admin.site.register(Link, LinkAdmin)
admin.site.register(NativeLink, NativeLinkAdmin)
