from django.contrib import admin

from apps.routes.models import Route, Station, Bus, ArrivalTime, UserPreference


class RouteAdmin(admin.ModelAdmin):
    list_display = ('name','origin','destination',)
    ordering = ('id',)

admin.site.register(Route, RouteAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('name','route',)
    ordering = ('id',)

admin.site.register(Station, StationAdmin)

class BusAdmin(admin.ModelAdmin):
    list_display = ('code','route',)
    ordering = ('id',)

admin.site.register(Bus, BusAdmin)

class ArrivalTimeAdmin(admin.ModelAdmin):
    list_display = ('time','bus','station',)
    ordering = ('id',)

admin.site.register(ArrivalTime, ArrivalTimeAdmin)

class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user','route','arrival_time',)
    ordering = ('id',)

admin.site.register(UserPreference, UserPreferenceAdmin)