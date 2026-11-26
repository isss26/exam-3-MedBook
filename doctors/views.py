from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Doctor, Specialization, Service
from .forms import DoctorForm, SpecializationForm, ServiceForm
from .permissions import AdminRequiredMixin, is_admin


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        doctors = Doctor.objects.filter(is_active=True).select_related('user', 'specialization').annotate(avg_rating=Avg('reviews__rating'), reviews_count=Count('reviews'))
        q = self.request.GET.get('q', '').strip()
        for word in q.split():
            doctors = doctors.filter(Q(user__first_name__icontains=word) | Q(user__last_name__icontains=word) | Q(user__username__icontains=word))

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
        doctors = Doctor.objects.select_related('user', 'specialization').prefetch_related('services')
        if not is_admin(self.request.user):
            doctors = doctors.filter(is_active=True)
        return doctors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.object
        now = timezone.localtime()
        context['free_slots'] = doctor.slots.filter(Q(date__gt=now.date()) | Q(date=now.date(), start_time__gt=now.time()), is_booked=False)
        context['reviews'] = doctor.reviews.select_related('author')
        context['rating'] = doctor.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
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

    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
        return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})

    def post(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
        doctor.is_active = False
        doctor.save(update_fields=['is_active'])
        messages.success(request, 'Врач деактивирован')
        return redirect('doctors:doctor_list')


class SpecializationListView(ListView):
    model = Specialization
    template_name = 'doctors/specialization_list.html'
    context_object_name = 'specializations'

    def get_queryset(self):
        return Specialization.objects.annotate(doctors_count=Count('doctors', filter=Q(doctors__is_active=True))).order_by('name')


class SpecializationCreateView(AdminRequiredMixin, CreateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'doctors/specialization_form.html'
    success_url = reverse_lazy('doctors:specialization_list')

    def form_valid(self, form):
        messages.success(self.request, 'Специализация добавлена')
        return super().form_valid(form)


class ServiceListView(ListView):
    model = Service
    template_name = 'doctors/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.annotate(doctors_count=Count('doctors', filter=Q(doctors__is_active=True))).order_by('name')


class ServiceCreateView(AdminRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'doctors/service_form.html'
    success_url = reverse_lazy('doctors:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Услуга добавлена')
        return super().form_valid(form)


class ServiceUpdateView(AdminRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'doctors/service_form.html'
    success_url = reverse_lazy('doctors:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Услуга обновлена')
        return super().form_valid(form)


class ServiceDeleteView(AdminRequiredMixin, DeleteView):
    model = Service
    template_name = 'doctors/service_confirm_delete.html'
    success_url = reverse_lazy('doctors:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Услуга удалена')
        return super().form_valid(form)