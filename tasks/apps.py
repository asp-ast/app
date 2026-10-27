from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Настраивает Django-приложение для управления задачами."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    verbose_name = 'Управление задачами'
