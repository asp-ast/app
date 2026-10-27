from dataclasses import dataclass
from typing import Sequence

from .models import Task


@dataclass(frozen=True)
class TaskStatistics:
    """Содержит рассчитанную статистику по набору задач."""

    total: int
    completed: int
    remaining: int
    total_hours: int
    completed_hours: int
    progress: int


def calculate_statistics(
    tasks: Sequence[Task],
) -> TaskStatistics:
    """
    Рассчитывает статистику по переданному набору задач.

    :param tasks: Последовательность объектов задач.

    :returns: Объект с рассчитанной статистикой.
    """
    total = len(tasks)

    completed_tasks = [
        task
        for task in tasks
        if task.status is not None
        and task.status.code == "done"
    ]

    completed = len(completed_tasks)
    remaining = total - completed

    total_hours = sum(
        task.estimated_hours
        for task in tasks
    )

    completed_hours = sum(
        task.estimated_hours
        for task in completed_tasks
    )

    if total_hours == 0:
        progress = 0
    else:
        progress = int(
            completed_hours / total_hours * 100,
        )

    return TaskStatistics(
        total=total,
        completed=completed,
        remaining=remaining,
        total_hours=total_hours,
        completed_hours=completed_hours,
        progress=progress,
    )


def get_task_details(
    task: Task,
) -> dict[str, object]:
    """
    Формирует словарь с подробной информацией о задаче.

    :param task: Объект задачи.

    :returns: Словарь с данными задачи для отображения.
    """
    status_name = (
        task.status.name
        if task.status is not None
        else "Не указан"
    )

    status_code = (
        task.status.code
        if task.status is not None
        else "—"
    )

    priority_name = (
        task.priority.name
        if task.priority is not None
        else "Не указан"
    )

    priority_level = (
        task.priority.level
        if task.priority is not None
        else "—"
    )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": status_name,
        "status_code": status_code,
        "priority": priority_name,
        "priority_level": priority_level,
        "estimated_hours": task.estimated_hours,
    }
