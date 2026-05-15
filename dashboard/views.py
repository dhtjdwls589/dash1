from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Task, Project, Comment, DirectMessage
from .forms import TaskForm, ProjectForm, CommentForm, DirectMessageForm


def staff_required(user):
    if not user.is_staff and not user.is_superuser:
        raise PermissionDenied


def get_unread_count(user):
    return DirectMessage.objects.filter(
        receiver=user,
        is_read=False
    ).count()


def get_visible_message_users(current_user):
    if current_user.is_superuser:
        return User.objects.exclude(
            id=current_user.id
        ).order_by("username")

    return User.objects.filter(
        is_superuser=True
    ).exclude(
        id=current_user.id
    ).order_by("username")


def get_users_with_unread(current_user):
    users = get_visible_message_users(current_user)

    result = []

    for user in users:
        unread_count = DirectMessage.objects.filter(
            sender=user,
            receiver=current_user,
            is_read=False
        ).count()

        result.append({
            "user": user,
            "unread_count": unread_count,
        })

    return result


def login_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard_index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard_index")
    else:
        form = AuthenticationForm()

    return render(request, "dashboard/login.html", {"form": form})


def register_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard_index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.is_superuser = False
            user.save()

            login(request, user)
            return redirect("dashboard_index")
    else:
        form = UserCreationForm()

    return render(request, "dashboard/register.html", {"form": form})


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
        staff_required(request.user)

        form = TaskForm(request.POST, request.FILES)

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
            "unread_message_count": get_unread_count(request.user),
        }
    )


@login_required
def projects_page(request):
    if request.method == "POST":
        staff_required(request.user)

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
            "unread_message_count": get_unread_count(request.user),
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
            "unread_message_count": get_unread_count(request.user),
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
            "unread_message_count": get_unread_count(request.user),
        }
    )


@login_required
def settings_page(request):
    return render(
        request,
        "dashboard/settings.html",
        {
            "unread_message_count": get_unread_count(request.user),
        }
    )


@login_required
def messages_page(request):
    first_user = get_visible_message_users(request.user).order_by("id").first()

    if first_user:
        return redirect("direct_chat_page", user_id=first_user.id)

    return render(
        request,
        "dashboard/messages.html",
        {
            "users_with_unread": get_users_with_unread(request.user),
            "unread_message_count": get_unread_count(request.user),
        }
    )


@login_required
def direct_chat_page(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    visible_user_ids = get_visible_message_users(request.user).values_list(
        "id",
        flat=True
    )

    if other_user.id not in visible_user_ids:
        return redirect("messages_page")

    chat_messages = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by("created_at")

    DirectMessage.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    form = DirectMessageForm()

    return render(
        request,
        "dashboard/direct_chat.html",
        {
            "users_with_unread": get_users_with_unread(request.user),
            "other_user": other_user,
            "chat_messages": chat_messages,
            "form": form,
            "unread_message_count": get_unread_count(request.user),
        }
    )


@login_required
def send_message_ajax(request, user_id):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "POST 요청만 가능합니다."
        }, status=405)

    other_user = get_object_or_404(User, id=user_id)

    visible_user_ids = get_visible_message_users(request.user).values_list(
        "id",
        flat=True
    )

    if other_user.id not in visible_user_ids:
        return JsonResponse({
            "success": False,
            "error": "메시지를 보낼 권한이 없습니다."
        }, status=403)

    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({
            "success": False,
            "error": "메시지를 입력하세요."
        }, status=400)

    message = DirectMessage.objects.create(
        sender=request.user,
        receiver=other_user,
        content=content
    )

    return JsonResponse({
        "success": True,
        "message": {
            "id": message.id,
            "content": message.content,
            "sender": message.sender.username,
            "is_mine": True,
            "created_at": message.created_at.strftime("%Y-%m-%d %H:%M"),
        }
    })


@login_required
def fetch_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    visible_user_ids = get_visible_message_users(request.user).values_list(
        "id",
        flat=True
    )

    if other_user.id not in visible_user_ids:
        return JsonResponse({
            "messages": [],
            "unread_count": get_unread_count(request.user),
        }, status=403)

    messages = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by("created_at")

    DirectMessage.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    data = []

    for message in messages:
        data.append({
            "id": message.id,
            "content": message.content,
            "sender": message.sender.username,
            "is_mine": message.sender_id == request.user.id,
            "created_at": message.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({
        "messages": data,
        "unread_count": get_unread_count(request.user),
    })


@login_required
def unread_message_summary(request):
    users_data = []
    total_count = 0

    users = get_visible_message_users(request.user)

    for user in users:
        count = DirectMessage.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()

        total_count += count

        users_data.append({
            "user_id": user.id,
            "username": user.username,
            "unread_count": count,
        })

    return JsonResponse({
        "total_unread_count": total_count,
        "users": users_data,
    })


@login_required
def unread_message_count(request):
    return JsonResponse({
        "unread_count": get_unread_count(request.user)
    })


@login_required
def delete_task(request, task_id):
    staff_required(request.user)

    task = get_object_or_404(Task, id=task_id)
    task.delete()

    return redirect("dashboard_index")


@login_required
def edit_task(request, task_id):
    staff_required(request.user)

    task = get_object_or_404(Task, id=task_id)

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
        form = TaskForm(instance=task)

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
    staff_required(request.user)

    task = get_object_or_404(Task, id=task_id)
    task.status = status
    task.save()

    return HttpResponse("OK")


@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

    return redirect("dashboard_index")


@login_required
def delete_comment(request, comment_id):
    staff_required(request.user)

    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()

    return redirect("dashboard_index")