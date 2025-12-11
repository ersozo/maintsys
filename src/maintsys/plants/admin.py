from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'is_active', 'asset_count', 'created_at']
    list_filter = ['is_active', 'city']
    search_fields = ['code', 'name', 'city']
    ordering = ['name']
