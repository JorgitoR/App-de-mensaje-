from django.contrib import admin

from .models import Channel, ChanelMensaje, ChanelUser

class ChannelMensajeInline(admin.TabularInline):
    model = ChanelMensaje
    extra = 1

class ChannelUserInline(admin.TabularInline):
    model = ChanelUser
    extra = 1

class ChanelAdmin(admin.ModelAdmin):
    inlines = [ChannelMensajeInline, ChannelUserInline]
    class Meta:
        model = Channel

admin.site.register(ChanelUser)
admin.site.register(Channel, ChanelAdmin)
admin.site.register(ChanelMensaje)