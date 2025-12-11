from django.contrib import admin
from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'plant', 'location', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'plant']
    search_fields = ['code', 'name', 'serial_number']
    ordering = ['plant', 'name']
    raw_id_fields = ['plant']
