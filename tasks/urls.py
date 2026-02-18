from django.urls import path
from tasks.views import (
    DashboardView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskMoveView,
    TaskCompleteView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path(
        "project/<int:project_id>/task/create/",
        TaskCreateView.as_view(),
        name="task-create",
    ),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/complete/", TaskCompleteView.as_view(), name="task-complete"),
    path(
        "task/<int:pk>/move/<str:direction>/", TaskMoveView.as_view(), name="task-move"
    ),
]
