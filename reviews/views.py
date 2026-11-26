from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from appointments.models import Appointment
from .forms import DoctorReviewForm
from .models import DoctorReview


COMPLETED = 'completed'


@login_required
def review_create(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.select_related('slot__doctor'), pk=appointment_id, patient=request.user,)

    doctor = appointment.slot.doctor

    if appointment.status != COMPLETED:
        messages.error(request, 'Отзыв можно оставить только после завершённого приёма')
        return redirect('doctors:doctor_detail', pk=doctor.pk)

    if DoctorReview.objects.filter(appointment=appointment).exists():
        messages.info(request, 'Вы уже оставили отзыв на этот приём')
        return redirect('doctors:doctor_detail', pk=doctor.pk)

    form = DoctorReviewForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.appointment = appointment
        review.author = request.user
        review.save()

        messages.success(request, 'Спасибо за отзыв!')
        return redirect('doctors:doctor_detail', pk=doctor.pk)

    return render(request, 'reviews/review_form.html', {'form': form, 'doctor': doctor,})


@login_required
def review_edit(request, pk):
    review = get_object_or_404(DoctorReview.objects.select_related('appointment__slot__doctor'), pk=pk, author=request.user,)
    doctor = review.appointment.slot.doctor
    form = DoctorReviewForm(request.POST or None, instance=review)

    if request.method == 'POST' and form.is_valid():
        form.save()

        messages.success(request, 'Отзыв обновлён')
        return redirect('doctors:doctor_detail', pk=doctor.pk)

    return render(request, 'reviews/review_form.html', {'form': form, 'doctor': doctor, 'review': review,})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(DoctorReview.objects.select_related('appointment__slot__doctor'), pk=pk, author=request.user,)
    doctor = review.appointment.slot.doctor

    if request.method == 'POST':
        review.delete()

        messages.success(request, 'Отзыв удалён')
        return redirect('doctors:doctor_detail', pk=doctor.pk)

    return render(request, 'reviews/review_confirm_delete.html', {'review': review,})
