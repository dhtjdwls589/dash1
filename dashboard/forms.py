from django import forms

from .models import Task, Project, Comment, DirectMessage


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

        widgets = {
            "project": forms.Select(attrs={
                "class": "form-input"
            }),
            "name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "작업명을 입력하세요"
            }),
            "memo": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "메모를 입력하세요",
                "rows": 4
            }),
            "progress": forms.NumberInput(attrs={
                "class": "form-input",
                "min": 0,
                "max": 100
            }),
            "status": forms.Select(attrs={
                "class": "form-input"
            }),
            "attachment": forms.ClearableFileInput(attrs={
                "class": "form-input"
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = [
            "name"
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "프로젝트 이름 입력"
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = [
            "content"
        ]

        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "댓글 입력..."
            })
        }


class DirectMessageForm(forms.ModelForm):
    class Meta:
        model = DirectMessage

        fields = [
            "content"
        ]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "message-input",
                "rows": 3,
                "placeholder": "메시지를 입력하세요..."
            })
        }