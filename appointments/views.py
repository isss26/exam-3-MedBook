from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Appointment, AppointmentHistory
from .forms import AppointmentForms
from doctors.models import Doctor
from schedules.models import TimeSlot


def change_status(appointment, new_status, user):
    AppointmentHistory.objects.create(appointment=appointment, old_status=appointment.status, new_status=new_status, changed_by=user)
    appointment.status = new_status
    appointment.save(update_fields=['status', 'updated_at'])


def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)


def available_slots(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id, is_active=True)
    slots = doctor.slots.filter(is_booked=False, date__gte=timezone.localdate()).order_by('date', 'start_time')
    return render(request, 'appointments/available_slots.html', {'doctor': doctor, 'slots': slots})


@login_required
def book_appointment(request, slot_id):
    slot = get_object_or_404(TimeSlot, pk=slot_id)

    if request.user.role != 'patient':
        messages.error(request, 'Записываться могут только пациенты')
        return redirect('appointments:available_slots', doctor_id=slot.doctor_id)

    if slot.is_booked or Appointment.objects.filter(slot=slot).exclude(status='cancelled').exists():
        messages.error(request, 'Этот слот уже занят')
        return redirect('appointments:available_slots', doctor_id=slot.doctor_id)

    if slot.date < timezone.localdate():
        messages.error(request, 'Этот слот уже прошёл')
        return redirect('appointments:available_slots', doctor_id=slot.doctor_id)

    if request.method == 'POST':
        form = AppointmentForms(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.slot = slot
            appointment.save()
            slot.is_booked = True
            slot.save(update_fields=['is_booked'])
            AppointmentHistory.objects.create(appointment=appointment, old_status='', new_status='pending', changed_by=request.user)
            messages.success(request, 'Вы записались на приём')
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentForms()

    return render(request, 'appointments/appointment_form.html', {'form': form, 'slot': slot})


class MyAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/my_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        appointments = Appointment.objects.filter(patient=self.request.user).select_related('slot', 'slot__doctor', 'slot__doctor__user')
        status = self.request.GET.get('status', '')
        if status:
            appointments = appointments.filter(status=status)
        return appointments.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Appointment.STATUS_CHOICES
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return Appointment.objects.select_related('patient', 'slot', 'slot__doctor', 'slot__doctor__user').prefetch_related('history')

    def test_func(self):
        appointment = self.get_object()
        user = self.request.user
        return appointment.patient == user or appointment.slot.doctor.user == user or is_admin(user)


class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForms
    template_name = 'appointments/appointment_form.html'

    def test_func(self):
        appointment = self.get_object()
        return appointment.patient == self.request.user and appointment.status == 'pending'

    def form_valid(self, form):
        messages.success(self.request, 'Комментарий обновлён')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('appointments:appointment_detail', kwargs={'pk': self.object.pk})


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointments:my_appointments')

    def test_func(self):
        appointment = self.get_object()
        return appointment.patient == self.request.user and appointment.status == 'cancelled'

    def form_valid(self, form):
        messages.success(self.request, 'Запись удалена')
        return super().form_valid(form)


@login_required
@require_POST
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)

    if appointment.status not in ['pending', 'confirmed']:
        messages.error(request, 'Эту запись нельзя отменить')
        return redirect('appointments:appointment_detail', pk=pk)

    change_status(appointment, 'cancelled', request.user)
    slot = appointment.slot
    slot.is_booked = False
    slot.save(update_fields=['is_booked'])
    messages.success(request, 'Запись отменена')
    return redirect('appointments:my_appointments')


@login_required
def doctor_appointments(request):
    if request.user.role != 'doctor':
        messages.error(request, 'Страница доступна только врачам')
        return redirect('doctors:doctor_list')

    appointments = Appointment.objects.filter(slot__doctor__user=request.user).select_related('patient', 'slot')
    status = request.GET.get('status', '')
    if status:
        appointments = appointments.filter(status=status)

    return render(request, 'appointments/doctor_appointments.html', {
        'appointments': appointments.order_by('slot__date', 'slot__start_time'),
        'statuses': Appointment.STATUS_CHOICES,
        'selected_status': status,
    })


@login_required
@require_POST
def confirm_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, slot__doctor__user=request.user)
    if appointment.status != 'pending':
        messages.error(request, 'Подтвердить можно только ожидающую запись')
    else:
        change_status(appointment, 'confirmed', request.user)
        messages.success(request, 'Запись подтверждена')
    return redirect('appointments:doctor_appointments')


@login_required
@require_POST
def complete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, slot__doctor__user=request.user)
    if appointment.status != 'confirmed':
        messages.error(request, 'Завершить можно только подтверждённую запись')
    else:
        change_status(appointment, 'completed', request.user)
        messages.success(request, 'Приём завершён')
    return redirect('appointments:doctor_appointments')


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total = Appointment.objects.aggregate(
        all=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        confirmed=Count('id', filter=Q(status='confirmed')),
        completed=Count('id', filter=Q(status='completed')),
        cancelled=Count('id', filter=Q(status='cancelled')),
    )
    by_doctor = Doctor.objects.select_related('user').annotate(
        all=Count('slots__appointments'),
        pending=Count('slots__appointments', filter=Q(slots__appointments__status='pending')),
        confirmed=Count('slots__appointments', filter=Q(slots__appointments__status='confirmed')),
        completed=Count('slots__appointments', filter=Q(slots__appointments__status='completed')),
        cancelled=Count('slots__appointments', filter=Q(slots__appointments__status='cancelled')),
    ).order_by('-all')
    return render(request, 'appointments/dashboard.html', {'total': total, 'by_doctor': by_doctor})