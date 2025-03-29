from django.contrib import admin
from logger.models import Device, DevicePosition, DevicePub


class DevicePubAdmin(admin.ModelAdmin):
    list_display = ['device', 'slug']


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'token',]


class DevicePositionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device, DeviceAdmin)
admin.site.register(DevicePosition, DevicePositionAdmin)
admin.site.register(DevicePub, DevicePubAdmin)
