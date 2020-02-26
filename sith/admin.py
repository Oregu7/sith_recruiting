from django.contrib import admin
from .models import Sith


@admin.register(Sith)
class SithAdmin(admin.ModelAdmin):
    oredering = ('name', 'planet', )
    search_fields = ('name', )
    list_display = ('name', 'planet', )
