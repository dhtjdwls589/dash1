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

    path("messages/", views.messages_page, name="messages_page"),
    path("messages/<int:user_id>/", views.direct_chat_page, name="direct_chat_page"),

    path(
        "fetch-messages/<int:user_id>/",
        views.fetch_messages,
        name="fetch_messages"
    ),

    path(
        "unread-message-count/",
        views.unread_message_count,
        name="unread_message_count"
    ),

    path(
        "unread-message-summary/",
        views.unread_message_summary,
        name="unread_message_summary"
    ),

    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),

    path(
        "update-status/<int:task_id>/<str:status>/",
        views.update_task_status,
        name="update_task_status"
    ),

    path(
        "add-comment/<int:task_id>/",
        views.add_comment,
        name="add_comment"
    ),

    path(
        "delete-comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment"
    ),
]