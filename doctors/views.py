
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from .models import Doctor, Specialization
from .forms import DoctorForm, SpecializationForm
from .permissions import AdminRequiredMixin, admin_required


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        doctors = Doctor.objects.filter(is_active=True)
        q = self.request.GET.get('q', '').strip()
        if q:
            doctors = doctors.filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(user__username__icontains=q))

        specialization = self.request.GET.get('specialization', '')

        if specialization.isdigit():
            doctors = doctors.filter(specialization_id=specialization)

        return doctors.order_by('user__last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['selected_spec'] = self.request.GET.get('specialization', '')
        return context


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctors/doctor_detail.html'
    context_object_name = 'doctor'

    def get_queryset(self):
        return Doctor.objects.filter(is_active=True).select_related('user', 'specialization').prefetch_related('services')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object
        context['free_slots'] = doctor.slots.filter(is_booked=False, date__gte=timezone.localdate())
        context['reviews'] = doctor.reviews.select_related('author')
        context['rating'] = doctor.reviews.aggregate(average=Avg('rating'), count=Count('id'))
        return context


class DoctorCreateView(AdminRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctors:doctor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Врач добавлен')
        return super().form_valid(form)


class DoctorUpdateView(AdminRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctors:doctor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные врача обновлены')
        return super().form_valid(form)


class DoctorDeactivateView(AdminRequiredMixin, View):

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.is_active = False
        doctor.save(update_fields=['is_active'])
        messages.success(request, 'Врач деактивирован')
        return redirect('doctors:doctor_list')


class SpecializationListView(ListView):
    model = Specialization
    template_name = 'doctors/specialization_list.html'
    context_object_name = 'specializations'


class SpecializationCreateView(AdminRequiredMixin, CreateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'doctors/specialization_form.html'
    success_url = reverse_lazy('doctors:specialization_list')

    def form_valid(self, form):
        messages.success(self.request, 'Специализация добавлена')
        return super().form_valid(form)
