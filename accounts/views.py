from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from repairs.models import RepairJob
from .forms import ClientRegistrationForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='Managers').exists():
            return reverse_lazy('dashboard')

        elif user.groups.filter(name='Mechanics').exists():
            return reverse_lazy('repairs:job_list')

        return reverse_lazy('client_profile')


class RegisterClientView(CreateView):
    template_name = 'accounts/register.html'
    form_class = ClientRegistrationForm
    success_url = reverse_lazy('client_profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ClientProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'client_profile'):
            client = user.client_profile
            context['client'] = client
            context['vehicles'] = client.vehicles.all()

            context['active_jobs'] = RepairJob.objects.filter(
                vehicle__client=client
            ).exclude(status='completed').order_by('-created_at')

            context['history_jobs'] = RepairJob.objects.filter(
                vehicle__client=client,
                status='completed'
            ).order_by('-updated_at')[:5]  # Последните 5

        return context