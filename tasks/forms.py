from django import forms
from tasks.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "deadline", "is_done"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Project Name"}
            ),
        }
