from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from doctors.models import Doctor
from doctors.permissions import doctor_required, is_doctor, is_admin
from .forms import TimeSlotForm
from .models import TimeSlot


def doctor_schedule(request, doctor_id):
    doctor = get_object_or_404(Doctor.objects.select_related('user', 'specialization'), pk=doctor_id)
    is_owner = is_doctor(request.user) and request.user.doctor.pk == doctor.pk
    if not doctor.is_active and not (is_owner or is_admin(request.user)):
        raise Http404

    slots = doctor.slots.filter(date__gte=timezone.localdate())

    if not is_owner:
        slots = slots.filter(is_booked=False)

    return render(request, 'schedules/doctor_schedule.html', {'doctor': doctor, 'slots': slots, 'is_owner': is_owner,})


@doctor_required
def slot_create(request):
    doctor = request.user.doctor
    form = TimeSlotForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        slot = form.save(commit=False)
        slot.doctor = doctor
        slot.save()

        messages.success(request, 'Слот создан')
        return redirect('schedules:doctor_schedule', doctor_id=doctor.pk)

    return render(request, 'schedules/slot_form.html', {'form': form,})


@require_POST
@doctor_required
def slot_delete(request, pk):
    slot = get_object_or_404(TimeSlot, pk=pk, doctor=request.user.doctor)

    if slot.is_booked:
        messages.error(request, 'Нельзя удалить слот, на который есть запись')
    else:
        slot.delete()
        messages.success(request, 'Слот удалён')

    return redirect('schedules:doctor_schedule', doctor_id=request.user.doctor.pk)
