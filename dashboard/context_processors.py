from .models import DirectMessage


def unread_messages(request):
    if request.user.is_authenticated:
        unread_message_count = DirectMessage.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
    else:
        unread_message_count = 0

    return {
        "unread_message_count": unread_message_count
    }