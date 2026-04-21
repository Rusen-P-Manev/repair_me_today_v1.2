import os
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from django.http import Http404
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import CarServiceUsers
from employees.models import Employee
from garage.models import Client, Vehicle
from repairs.models import RepairJob, PartOrder, Service, RepairService
from invoicing.models import ShopProfile
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
            ).order_by('-updated_at')[:5]

        return context


class AddDemoDataView(View):
    def get(self, request, *args, **kwargs):
        expected_token = os.getenv('DEMO_SEED_TOKEN', 'softuni2026')
        provided_token = request.GET.get('token')

        if provided_token != expected_token:
            raise Http404("Страницата не е намерена.")

        if Employee.objects.exists():
            messages.warning(request, "Демо данните са вече в системата!")
            return redirect('login')

        managers_group, _ = Group.objects.get_or_create(name='Managers')
        mechanics_group, _ = Group.objects.get_or_create(name='Mechanics')

        client_ct = ContentType.objects.get_for_model(Client)
        vehicle_ct = ContentType.objects.get_for_model(Vehicle)
        repair_ct = ContentType.objects.get_for_model(RepairJob)
        part_ct = ContentType.objects.get_for_model(PartOrder)

        mechanics_permissions = Permission.objects.filter(
            content_type__in=[client_ct, vehicle_ct, repair_ct, part_ct],
            codename__in=[
                'add_client', 'change_client', 'add_vehicle', 'change_vehicle',
                'add_repairjob', 'change_repairjob', 'add_partorder', 'change_partorder'
            ]
        )
        mechanics_group.permissions.set(mechanics_permissions)

        managers_permissions = Permission.objects.filter(
            content_type__in=[client_ct, vehicle_ct, repair_ct, part_ct]
        )
        managers_group.permissions.set(managers_permissions)

        if not ShopProfile.objects.exists():
            ShopProfile.objects.create(
                name='Repair Me Today ООД',
                eik='123456789',
                vat_number='BG123456789',
                address='гр. София, бул. Черен път 100',
                mol='Румен Симеонов',
                iban='BG12DEMO12345678901234'
            )

        service_oil = Service.objects.create(
            name='Смяна на масло и филтри',
            price=45.00
        )
        service_diag = Service.objects.create(
            name='Компютърна диагностика',
            price=60.00
        )
        service_brakes = Service.objects.create(
            name='Смяна на накладки',
            price=55.00
        )

        if not CarServiceUsers.objects.filter(username='admin').exists():
            CarServiceUsers.objects.create_superuser('admin', 'admin@repairme.com', 'admin')

        manager_user = CarServiceUsers.objects.create_user(
            username='manager',
            email='manager@repairme.com',
            password='manager_password',
            first_name='Румен',
            last_name='Симеонов'
        )
        manager_emp = Employee.objects.create(
            user=manager_user,
            first_name='Румен',
            last_name='Симеонов',
            position='Управител',
            phone_number='0888111222'
        )

        mechanic_user = CarServiceUsers.objects.create_user(
            username='mechanic',
            email='mechanic@repairme.com',
            password='mechanic_password',
            first_name='Димитър',
            last_name='Желязков'
        )
        mechanic_emp = Employee.objects.create(
            user=mechanic_user,
            first_name='Димитър',
            last_name='Желязков',
            position='Автомонтьор',
            phone_number='0888333444'
        )

        demo_client_user = CarServiceUsers.objects.create_user(
            username='demo_client',
            email='client@example.com',
            password='client_password',
            first_name='Георги',
            last_name='Петров'
        )
        demo_client = Client.objects.create(
            user=demo_client_user,
            first_name='Георги',
            last_name='Петров',
            phone_number='0899555666',
            address_city='София',
            address_street='ул. Лунен пейзаж 10'
        )

        demo_vehicle = Vehicle.objects.create(
            client=demo_client,
            make='BMW',
            model='530d',
            year=2018,
            vin='WBAJS31000DEMO123',
            vehicle_registration_number='CB1234AB'
        )

        job = RepairJob.objects.create(
            vehicle=demo_vehicle,
            received_by=manager_emp,
            repaired_by=mechanic_emp,
            problem_description='Светеща лампа за проверка на двигателя.',
            status='in_progress'
        )

        RepairService.objects.create(repair_job=job, service=service_oil, quantity=1)
        RepairService.objects.create(repair_job=job, service=service_diag, quantity=1)

        messages.success(request, "Данните са заредени!")
        return redirect('login')