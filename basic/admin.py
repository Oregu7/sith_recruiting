from django.contrib import admin
from .models import Planet


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    oredering = ('name', )
    search_fields = ('name', )
    list_display = ('name', )