from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')


def is_doctor(user):
    return (user.is_authenticated and user.role == 'doctor' and hasattr(user, 'doctor') and user.doctor.is_active)


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def doctor_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not is_doctor(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return is_admin(self.request.user)


class DoctorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return is_doctor(self.request.user)