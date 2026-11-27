from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        if not username or not email or not password1:
            return render(request, 'register.html', {"error": "Username, email and password are required"})
        if password1 != password2:
            return render(request, 'register.html', {"error": "Passwords do not match"})
        if len(password1) < 8:
            return render(request, 'register.html', {"error": "Password must be at least 8 characters long"})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {"error": "Username already exists"})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {"error": "Email already exists"})
        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = request.build_absolute_uri(reverse('confirm_email', args=[uidb64, token]))
        try:
            send_mail("Confirm your email", f"Hi {user.username}!\nConfirm your email: {link}", None, [user.email])
        except Exception:
            user.delete()
            return render(request, 'register.html', {"error": "Could not send email, try again"})
        return render(request, 'login.html', {"message": "We sent a confirmation link to your email"})
    return render(request, 'register.html')


def confirm_email(request, uidb64, token):
    try:
        user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except (TypeError, ValueError, User.DoesNotExist):
        return render(request, 'login.html', {"error": "Confirmation link is invalid"})
    if not default_token_generator.check_token(user, token):
        return render(request, 'login.html', {"error": "Confirmation link is invalid"})
    user.is_active = True
    user.save()
    return render(request, 'login.html', {"message": "Email confirmed, now you can login"})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if not user:
            if User.objects.filter(username=username, is_active=False).exists():
                return render(request, 'login.html', {"error": "Confirm your email first"})
            return render(request, 'login.html', {"error": "Invalid username or password"})
        login(request, user)
        return redirect(request.GET.get("next") or 'home')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('home')


@login_required
def profile(request):
    appointments = request.user.appointments.select_related('slot', 'slot__doctor', 'slot__doctor__user').order_by('-created_at')[:5]  # ← ИЗМЕНЕНО
    return render(request, 'profile.html', {'appointments': appointments})  # ← ИЗМЕНЕНО


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get("old_password", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        if not request.user.check_password(old_password):
            return render(request, 'change_password.html', {"error": "Old password is wrong"})
        if password1 != password2:
            return render(request, 'change_password.html', {"error": "Passwords do not match"})
        if len(password1) < 8:
            return render(request, 'change_password.html', {"error": "Password must be at least 8 characters long"})
        request.user.set_password(password1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect('profile')
    return render(request, 'change_password.html')