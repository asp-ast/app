from django.test import TestCase
from django.urls import reverse

from .models import Task, TaskPriority, TaskStatus
from .services import calculate_statistics, get_task_details


class TaskModelTests(TestCase):
    """Проверяет работу моделей приложения."""

    def setUp(self) -> None:
        """Создаёт тестовые справочные данные."""
        self.status_todo = TaskStatus.objects.create(
            name="К выполнению",
            code="todo",
        )
        self.status_done = TaskStatus.objects.create(
            name="Выполнено",
            code="done",
        )
        self.priority_high = TaskPriority.objects.create(
            name="Высокий",
            level=3,
        )

    def test_task_string_representation(self) -> None:
        """Проверяет строковое представление задачи."""
        task = Task.objects.create(
            title="Тестовая задача",
            status=self.status_todo,
            priority=self.priority_high,
            estimated_hours=2,
        )

        self.assertEqual(
            str(task),
            "Тестовая задача",
        )

    def test_set_null_status(self) -> None:
        """Проверяет обнуление статуса после его удаления."""
        task = Task.objects.create(
            title="Тестовая задача",
            status=self.status_todo,
            priority=self.priority_high,
            estimated_hours=2,
        )

        self.status_todo.delete()
        task.refresh_from_db()

        self.assertIsNone(task.status)


class TaskServiceTests(TestCase):
    """Проверяет бизнес-логику приложения."""

    def setUp(self) -> None:
        """Создаёт тестовые данные."""
        self.status_todo = TaskStatus.objects.create(
            name="К выполнению",
            code="todo",
        )
        self.status_done = TaskStatus.objects.create(
            name="Выполнено",
            code="done",
        )
        self.priority = TaskPriority.objects.create(
            name="Высокий",
            level=3,
        )

    def test_calculate_statistics(self) -> None:
        """Проверяет расчёт общей статистики."""
        task_one = Task.objects.create(
            title="Первая задача",
            status=self.status_done,
            priority=self.priority,
            estimated_hours=3,
        )
        task_two = Task.objects.create(
            title="Вторая задача",
            status=self.status_todo,
            priority=self.priority,
            estimated_hours=7,
        )

        statistics = calculate_statistics(
            [task_one, task_two],
        )

        self.assertEqual(statistics.total, 2)
        self.assertEqual(statistics.completed, 1)
        self.assertEqual(statistics.remaining, 1)
        self.assertEqual(statistics.total_hours, 10)
        self.assertEqual(statistics.completed_hours, 3)
        self.assertEqual(statistics.progress, 30)

    def test_calculate_statistics_with_zero_hours(self) -> None:
        """Проверяет расчёт прогресса при нулевой оценке часов."""
        task = Task.objects.create(
            title="Задача без оценки",
            status=self.status_todo,
            priority=self.priority,
            estimated_hours=0,
        )

        statistics = calculate_statistics([task])

        self.assertEqual(statistics.progress, 0)

    def test_get_task_details(self) -> None:
        """Проверяет формирование словаря с данными задачи."""
        task = Task.objects.create(
            title="Подробная задача",
            description="Описание задачи",
            status=self.status_done,
            priority=self.priority,
            estimated_hours=5,
        )

        details = get_task_details(task)

        self.assertEqual(
            details["title"],
            "Подробная задача",
        )
        self.assertEqual(
            details["status"],
            "Выполнено",
        )
        self.assertEqual(
            details["status_code"],
            "done",
        )
        self.assertEqual(
            details["priority"],
            "Высокий",
        )
        self.assertEqual(
            details["priority_level"],
            3,
        )
        self.assertEqual(
            details["estimated_hours"],
            5,
        )


class TaskViewTests(TestCase):
    """Проверяет HTTP-представления приложения."""

    def setUp(self) -> None:
        """Создаёт тестовые данные для представлений."""
        self.status = TaskStatus.objects.create(
            name="К выполнению",
            code="todo",
        )
        self.priority = TaskPriority.objects.create(
            name="Высокий",
            level=3,
        )
        self.task = Task.objects.create(
            title="Задача для страницы",
            status=self.status,
            priority=self.priority,
            estimated_hours=4,
        )

    def test_task_list_view(self) -> None:
        """Проверяет страницу со списком задач."""
        response = self.client.get(
            reverse("task_list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Задача для страницы",
        )

    def test_task_detail_view(self) -> None:
        """Проверяет страницу с подробностями задачи."""
        response = self.client.get(
            reverse(
                "task_detail",
                kwargs={"task_id": self.task.id},
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Задача для страницы",
        )

    def test_task_detail_missing_task(self) -> None:
        """Проверяет страницу ошибки для отсутствующей задачи."""
        response = self.client.get(
            reverse(
                "task_detail",
                kwargs={"task_id": 999999},
            ),
        )

        self.assertEqual(response.status_code, 404)
