from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("created_at", "full_name", "service", "comuna", "status", "phone")
    list_filter = ("status", "service", "comuna", "property_type")
    search_fields = ("full_name", "phone", "email", "message")
    ordering = ("-created_at",)
