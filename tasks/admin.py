from django.contrib import admin

from .models import Task, TaskPriority, TaskStatus


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    """Настраивает административный интерфейс для статусов задач."""

    list_display = (
        "name",
        "code",
    )


@admin.register(TaskPriority)
class TaskPriorityAdmin(admin.ModelAdmin):
    """Настраивает административный интерфейс для приоритетов задач."""

    list_display = (
        "name",
        "level",
    )
    ordering = (
        "level",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Настраивает административный интерфейс для задач."""

    list_display = (
        "title",
        "status",
        "priority",
        "estimated_hours",
        "created_at",
    )
    list_filter = (
        "status",
        "priority",
    )
    search_fields = (
        "title",
        "description",
    )
    list_select_related = (
        "status",
        "priority",
    )
