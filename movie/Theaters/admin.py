from django.contrib import admin
from .models import Theater

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name',  'location',  'admin')
    search_fields = ('name',  'location')
