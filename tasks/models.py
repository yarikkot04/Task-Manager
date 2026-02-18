from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    priority = models.PositiveIntegerField(db_index=True, default=0)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["priority"]

    def save(self, *args, **kwargs):
        if not self.priority:
            max_prio = Task.objects.filter(project=self.project).aggregate(
                Max("priority")
            )["priority__max"]
            self.priority = (max_prio or 0) + 1
        super().save(*args, **kwargs)

    @property
    def short_title(self):
        text = self.title.split("\n")[0][:50]
        if len(self.title) > 50:
            return text + "..."
        return text

    def __str__(self):
        return self.short_title
