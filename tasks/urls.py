from django.urls import path
from tasks.views import (
    DashboardView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskMoveView,
    TaskCompleteView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
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
    path("project/create/", ProjectCreateView.as_view(), name="project-create"),
    path(
        "project/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
]
