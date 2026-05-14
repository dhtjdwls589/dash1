from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Task, Project
from .forms import TaskForm, ProjectForm


def login_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard_index")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("dashboard_index")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "dashboard/login.html",
        {
            "form": form,
        }
    )


def register_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard_index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.is_staff = True
            user.is_superuser = True
            user.save()

            login(request, user)

            return redirect("dashboard_index")

    else:
        form = UserCreationForm()

    return render(
        request,
        "dashboard/register.html",
        {
            "form": form,
        }
    )


def logout_page(request):
    logout(request)

    return redirect("login")


@login_required
def index(request):
    projects = Project.objects.all()

    selected_project_id = request.GET.get("project")
    search_query = request.GET.get("q", "").strip()

    tasks = Task.objects.select_related("project").all().order_by("-created_at")

    if selected_project_id:
        tasks = tasks.filter(project_id=selected_project_id)

    if search_query:
        tasks = tasks.filter(
            Q(name__icontains=search_query) |
            Q(memo__icontains=search_query) |
            Q(project__name__icontains=search_query)
        )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            return redirect("dashboard_index")

    else:
        form = TaskForm()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="완료").count()
    in_progress_tasks = tasks.filter(status="진행 중").count()
    todo_tasks_count = tasks.filter(status="예정").count()

    average_progress = int(
        sum(task.progress for task in tasks) / total_tasks
    ) if total_tasks > 0 else 0

    return render(
        request,
        "dashboard/index.html",
        {
            "tasks": tasks,
            "projects": projects,
            "form": form,

            "selected_project_id": selected_project_id,
            "search_query": search_query,

            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "todo_tasks_count": todo_tasks_count,
            "average_progress": average_progress,

            "todo_tasks": tasks.filter(status="예정"),
            "progress_tasks": tasks.filter(status="진행 중"),
            "done_tasks": tasks.filter(status="완료"),
        }
    )


@login_required
def projects_page(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("projects_page")

    else:
        form = ProjectForm()

    projects = Project.objects.all().order_by("-created_at")

    project_cards = []

    for project in projects:
        tasks = project.tasks.all()

        total = tasks.count()
        completed = tasks.filter(status="완료").count()

        average_progress = int(
            sum(task.progress for task in tasks) / total
        ) if total > 0 else 0

        project_cards.append({
            "project": project,
            "total": total,
            "completed": completed,
            "average_progress": average_progress,
        })

    return render(
        request,
        "dashboard/projects.html",
        {
            "project_cards": project_cards,
            "form": form,
        }
    )


@login_required
def tasks_page(request):
    search_query = request.GET.get("q", "").strip()

    tasks = Task.objects.select_related("project").all().order_by("-created_at")

    if search_query:
        tasks = tasks.filter(
            Q(name__icontains=search_query) |
            Q(memo__icontains=search_query) |
            Q(project__name__icontains=search_query)
        )

    return render(
        request,
        "dashboard/tasks.html",
        {
            "tasks": tasks,
            "search_query": search_query,
            "total_tasks": tasks.count(),
        }
    )


@login_required
def stats_page(request):
    tasks = Task.objects.all()
    projects = Project.objects.all()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="완료").count()
    in_progress_tasks = tasks.filter(status="진행 중").count()
    todo_tasks_count = tasks.filter(status="예정").count()

    average_progress = int(
        sum(task.progress for task in tasks) / total_tasks
    ) if total_tasks > 0 else 0

    return render(
        request,
        "dashboard/stats.html",
        {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "todo_tasks_count": todo_tasks_count,
            "average_progress": average_progress,
            "project_count": projects.count(),
        }
    )


@login_required
def settings_page(request):
    return render(
        request,
        "dashboard/settings.html"
    )


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    task.delete()

    return redirect("dashboard_index")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == "POST":
        form = TaskForm(
            request.POST,
            request.FILES,
            instance=task
        )

        if form.is_valid():
            form.save()

            return redirect("dashboard_index")

    else:
        form = TaskForm(
            instance=task
        )

    return render(
        request,
        "dashboard/edit.html",
        {
            "form": form,
            "task": task,
        }
    )


@login_required
def update_task_status(request, task_id, status):
    task = get_object_or_404(
        Task,
        id=task_id
    )

    task.status = status
    task.save()

    return HttpResponse("OK")