from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Project, Task


class TaskFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        self.client = Client()
        self.client.force_login(self.user)

        self.project = Project.objects.create(name="Test Project", user=self.user)

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_create_task(self):
        url = reverse("task-create", args=[self.project.id])
        data = {"title": "New Test Task", "deadline": "2025-12-31"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Task.objects.filter(title="New Test Task").exists())

        self.assertTemplateUsed(response, "tasks/partials/task_row.html")

    def test_update_task(self):
        task = Task.objects.create(title="Old Title", project=self.project, priority=1)

        url = reverse("task-update", args=[task.id])
        data = {"title": "Updated Title", "deadline": "2026-01-01"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Title")

    def test_complete_task(self):
        task = Task.objects.create(
            title="Task to complete", project=self.project, is_done=False
        )

        url = reverse("task-complete", args=[task.id])

        self.client.post(url)

        task.refresh_from_db()
        self.assertTrue(task.is_done)

        self.client.post(url)
        task.refresh_from_db()
        self.assertFalse(task.is_done)

    def test_move_task(self):
        task1 = Task.objects.create(title="Task 1", project=self.project, priority=1)
        task2 = Task.objects.create(title="Task 2", project=self.project, priority=2)

        url = reverse("task-move", args=[task2.id, "up"])
        self.client.post(url)

        task1.refresh_from_db()
        task2.refresh_from_db()

        self.assertEqual(task2.priority, 1)
        self.assertEqual(task1.priority, 2)

    def test_delete_task(self):
        task = Task.objects.create(title="Delete Me", project=self.project)

        url = reverse("task-delete", args=[task.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_cannot_access_other_users_project(self):
        other_user = User.objects.create_user(username="other", password="password")
        other_project = Project.objects.create(name="Other Project", user=other_user)

        url = reverse("task-create", args=[other_project.id])
        response = self.client.post(url, {"title": "Hacker Task"})

        self.assertEqual(response.status_code, 404)


class ProjectViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mainuser", password="password")

        self.other_user = User.objects.create_user(
            username="hacker", password="password"
        )

        self.client = Client()
        self.client.force_login(self.user)

        self.project = Project.objects.create(name="My Project", user=self.user)

    def test_project_create_success(self):
        url = reverse("project-create")
        data = {"name": "New Test Project"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Project.objects.filter(name="New Test Project", user=self.user).exists()
        )

        self.assertTemplateUsed(response, "tasks/partials/project_card.html")

        self.assertIn("project", response.context)

    def test_project_update_success(self):
        url = reverse("project-update", args=[self.project.id])
        data = {"name": "Renamed Project"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Renamed Project")

        self.assertTemplateUsed(response, "tasks/partials/project_header.html")

    def test_project_update_access_denied(self):
        other_project = Project.objects.create(
            name="Other Project", user=self.other_user
        )

        url = reverse("project-update", args=[other_project.id])
        data = {"name": "Hacked Name"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)

        other_project.refresh_from_db()
        self.assertEqual(other_project.name, "Other Project")

    def test_project_delete_success(self):
        url = reverse("project-delete", args=[self.project.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.content, b"")

        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_project_delete_access_denied(self):
        other_project = Project.objects.create(
            name="Dont Touch This", user=self.other_user
        )

        url = reverse("project-delete", args=[other_project.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

        self.assertTrue(Project.objects.filter(id=other_project.id).exists())

    def test_anonymous_user_cannot_create_project(self):
        self.client.logout()

        url = reverse("project-create")
        response = self.client.post(url, {"name": "Anon Project"})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))
