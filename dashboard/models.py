from django.db import models


class Project(models.Model):

    name = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Task(models.Model):

    STATUS_CHOICES = [
        ("예정", "예정"),
        ("진행 중", "진행 중"),
        ("완료", "완료"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="예정"
    )

    progress = models.IntegerField(
        default=0
    )

    memo = models.TextField(
        blank=True,
        null=True
    )

    attachment = models.FileField(
        upload_to="attachments/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name