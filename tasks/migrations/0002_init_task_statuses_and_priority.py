from django.db import migrations


def create_initial_data(apps, schema_editor) -> None:
    """Создаёт начальные статусы и приоритеты задач."""
    TaskStatus = apps.get_model("tasks", "TaskStatus")
    TaskPriority = apps.get_model("tasks", "TaskPriority")

    TaskStatus.objects.bulk_create(
        [
            TaskStatus(
                name="К выполнению",
                code="todo",
            ),
            TaskStatus(
                name="В процессе",
                code="in_progress",
            ),
            TaskStatus(
                name="Выполнено",
                code="done",
            ),
        ]
    )

    TaskPriority.objects.bulk_create(
        [
            TaskPriority(
                name="Низкий",
                level=1,
            ),
            TaskPriority(
                name="Средний",
                level=2,
            ),
            TaskPriority(
                name="Высокий",
                level=3,
            ),
        ]
    )


def delete_initial_data(apps, schema_editor) -> None:
    """Удаляет созданные начальные статусы и приоритеты."""
    TaskStatus = apps.get_model("tasks", "TaskStatus")
    TaskPriority = apps.get_model("tasks", "TaskPriority")

    TaskStatus.objects.filter(
        code__in=[
            "todo",
            "in_progress",
            "done",
        ]
    ).delete()

    TaskPriority.objects.filter(
        level__in=[1, 2, 3],
    ).delete()


class Migration(migrations.Migration):
    """Добавляет начальные данные для справочников задач."""

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_initial_data,
            delete_initial_data,
        ),
    ]
