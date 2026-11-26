from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')


def is_doctor(user):
    return (user.is_authenticated and user.role == 'doctor' and hasattr(user, 'doctor'))


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user

        if user.is_superuser:
            return True

        return user.role == 'admin'


class DoctorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user

        return user.role == 'doctor' and hasattr(user, 'doctor')