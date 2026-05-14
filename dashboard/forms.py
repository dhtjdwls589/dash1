from django import forms
from .models import Task, Project, Comment


class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "project",
            "name",
            "memo",
            "progress",
            "status",
            "attachment",
        ]


class ProjectForm(forms.ModelForm):

    class Meta:

        model = Project

        fields = [
            "name"
        ]


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = [
            "content"
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "댓글 입력..."
                }
            )
        }