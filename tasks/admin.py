from django.contrib import admin
from tasks.models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("short_title", "project", "priority", "is_done", "deadline")
    list_display_links = ("short_title",)
    list_filter = ("priority", "is_done", "project")
    ordering = ("priority",)
