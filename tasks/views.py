from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Project, Task
from tasks.forms import TaskForm, ProjectForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import View
from django.db import transaction


class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasks/dashboard.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).prefetch_related("tasks")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/partials/task_row.html"

    def form_valid(self, form):
        project = get_object_or_404(
            Project, pk=self.kwargs["project_id"], user=self.request.user
        )
        form.instance.project = project
        self.object = form.save()
        return render(self.request, self.template_name, {"task": self.object})

    def form_invalid(self, form):
        return HttpResponse("Error in form", status=400)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/partials/task_row.html"

    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, self.template_name, {"task": self.object})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_queryset(self):
        return Task.objects.filter(project__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("")


class TaskMoveView(View):
    def post(self, request, pk, direction):
        task = get_object_or_404(Task, pk=pk)
        project = task.project

        if direction == "up":
            neighbor = (
                project.tasks.filter(priority__lt=task.priority)
                .order_by("-priority")
                .first()
            )
        else:
            neighbor = (
                project.tasks.filter(priority__gt=task.priority)
                .order_by("priority")
                .first()
            )

        if neighbor:
            with transaction.atomic():
                task.priority, neighbor.priority = neighbor.priority, task.priority
                task.save()
                neighbor.save()

        return render(
            request,
            "tasks/partials/task_list_content.html",
            {"tasks": project.tasks.all()},
        )


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__user=request.user)
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])

        return render(request, "tasks/partials/task_row.html", {"task": task})


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/partials/project_card.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return render(self.request, self.template_name, {"project": self.object})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "tasks/partials/project_header.html"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, self.template_name, {"project": self.object})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse("")
