from django.contrib import admin

from .models import School, Location


class SchoolAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(School, SchoolAdmin)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Location, LocationAdmin)
