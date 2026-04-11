from django.shortcuts import render
from django.views.generic import TemplateView
from repairs.models import RepairJob
from garage.models import Vehicle, Client


class ViewDashboard(TemplateView):
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_jobs'] = RepairJob.objects.exclude(status='completed')
        context['active_jobs_count'] = context['active_jobs'].count()
        context['completed_jobs_count'] = RepairJob.objects.filter(status='completed').count()
        context['total_clients'] = Client.objects.count()
        context['total_vehicles'] = Vehicle.objects.count()

        context['recent_jobs'] = context['active_jobs'].order_by('-created_at')

        return context