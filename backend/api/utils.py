from users.models import Subscription


def check_subscribed(request, obj):
    if request and not request.user.is_anonymous:
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()
    return False
