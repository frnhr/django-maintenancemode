

def is_staff(request):
    return hasattr(request, 'user') and request.user.is_staff


def is_superuser(request):
    return hasattr(request, 'user') and request.user.is_superuser
