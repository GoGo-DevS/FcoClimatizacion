from django.contrib import admin
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "alt", "order")
    ordering = ("order",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "comuna", "project_type", "brand", "btu", "featured", "created_at")
    list_filter = ("featured", "project_type", "brand", "region")
    search_fields = ("title", "comuna", "brand", "description")
    inlines = [ProjectImageInline]
