from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "status",
        "progress",
        "created_at",
    )

    list_filter = (
        "project",
        "status",
    )

    search_fields = (
        "name",
        "memo",
    )