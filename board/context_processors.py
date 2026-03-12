from .models import Messages

def unread_messages_count(request):
    if request.user.is_authenticated:
        unread_count = Messages.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
    else:
        unread_count = 0

    return {
        'unread_count': unread_count
    }