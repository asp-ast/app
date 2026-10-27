from django.db import models


class TaskStatus(models.Model):
    """Модель: Статус задачи."""

    name = models.CharField(
        verbose_name="Название",
        max_length=50,
    )
    code = models.CharField(
        verbose_name="Код",
        max_length=50,
        unique=True,
    )

    class Meta:
        """Метаданные модели статуса задачи."""

        verbose_name = "Статус задачи"
        verbose_name_plural = "Статусы задач"
        ordering = ("name",)

    def __str__(self) -> str:
        """Возвращает строковое представление статуса задачи."""
        return self.name


class TaskPriority(models.Model):
    """Модель: Приоритет задачи."""

    name = models.CharField(
        verbose_name="Название",
        max_length=50,
    )
    level = models.PositiveIntegerField(
        verbose_name="Уровень",
        unique=True,
    )

    class Meta:
        """Метаданные модели приоритета задачи."""

        verbose_name = "Приоритет задачи"
        verbose_name_plural = "Приоритеты задач"
        ordering = ("level",)

    def __str__(self) -> str:
        """Возвращает строковое представление приоритета задачи."""
        return self.name


class Task(models.Model):
    """Модель: Задача."""

    title = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    status = models.ForeignKey(
        TaskStatus,
        verbose_name="Статус",
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks",
    )
    priority = models.ForeignKey(
        TaskPriority,
        verbose_name="Приоритет",
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks",
    )
    estimated_hours = models.PositiveIntegerField(
        verbose_name="Оценка в часах",
        default=1,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        """Метаданные модели задачи."""

        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ("-priority__level", "-created_at")

        constraints = [
            models.CheckConstraint(
                condition=models.Q(estimated_hours__gte=0),
                name="task_estimated_hours_non_negative",
            ),
        ]

    def __str__(self) -> str:
        """Возвращает строковое представление задачи."""
        return self.title
