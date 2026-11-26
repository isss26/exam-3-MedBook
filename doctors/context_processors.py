from .permissions import is_admin, is_doctor


def roles(request):
    return {'is_admin': is_admin(request.user), 'is_doctor': is_doctor(request.user)}