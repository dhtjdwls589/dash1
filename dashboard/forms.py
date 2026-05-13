from django import forms

from .models import Task, Project


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "project",
            "name",
            "status",
            "progress",
            "memo",
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

            "status": forms.Select(attrs={
                "class": "form-input"
            }),

            "progress": forms.NumberInput(attrs={
                "class": "form-input",
                "min": 0,
                "max": 100
            }),

            "memo": forms.Textarea(attrs={
                "class": "form-input memo-input",
                "placeholder": "메모를 입력하세요"
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