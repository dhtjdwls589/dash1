from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_page, name="logout"),

    path("", views.index, name="dashboard_index"),
    path("projects/", views.projects_page, name="projects_page"),
    path("tasks/", views.tasks_page, name="tasks_page"),
    path("stats/", views.stats_page, name="stats_page"),
    path("settings/", views.settings_page, name="settings_page"),

    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),

    path(
        "update-status/<int:task_id>/<str:status>/",
        views.update_task_status,
        name="update_task_status"
    ),
]