from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Task
from .services import calculate_statistics, get_task_details


def task_list(request: HttpRequest) -> HttpResponse:
    """Отображает список задач и рассчитанную статистику."""
    tasks = list(
        Task.objects
        .select_related("status", "priority")
        .all()
    )

    statistics = calculate_statistics(tasks)

    context: dict[str, object] = {
        "tasks": tasks,
        "statistics": statistics,
    }

    return render(
        request,
        "tasks/list.html",
        context,
    )


def task_detail(
    request: HttpRequest,
    task_id: int,
) -> HttpResponse:
    """Отображает подробную информацию об одной задаче."""
    try:
        task = (
            Task.objects
            .select_related("status", "priority")
            .get(id=task_id)
        )
    except Task.DoesNotExist as exc:
        raise Http404("Задача не найдена") from exc

    details = get_task_details(task)

    context: dict[str, object] = {
        "task": task,
        "details": details,
    }

    return render(
        request,
        "tasks/detail.html",
        context,
    )
