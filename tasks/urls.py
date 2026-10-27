from django.urls import URLPattern, path

from . import views


urlpatterns: list[URLPattern] = [
    path(
        "",
        views.task_list,
        name="task_list",
    ),
    path(
        "tasks/<int:task_id>/",
        views.task_detail,
        name="task_detail",
    ),
]
