from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Client, Vehicle
from .forms import ClientForm, VehicleForm
from accounts.mixins import MechanicRequiredMixin, ManagerRequiredMixin


# clients -->
class ViewClientList(MechanicRequiredMixin, ListView):
    model = Client
    template_name = 'garage/client_list.html'
    context_object_name = 'clients'
    ordering = ['-id']


class ViewClientCreate(MechanicRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'garage/client_form.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.success(self.request, "Клиентът беше добавен успешно!")
        response = super().form_valid(form)
        if 'save_and_add_vehicle' in self.request.POST:
            return redirect(f"{reverse('garage:vehicle_create')}?client_id={self.object.id}")
        return response


class ViewClientUpdate(MechanicRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'garage/client_form.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.success(self.request, "Данните на клиента бяха обновени!")
        response = super().form_valid(form)
        if 'save_and_add_vehicle' in self.request.POST:
            return redirect(f"{reverse('garage:vehicle_create')}?client_id={self.object.id}")
        return response


class ViewClientDelete(ManagerRequiredMixin, DeleteView):
    model = Client
    template_name = 'garage/client_delete_confirmation.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.warning(self.request, "Клиентът беше изтрит от системата.")
        return super().form_valid(form)


# vehicles -->
class ViewVehicleList(MechanicRequiredMixin, ListView):
    model = Vehicle
    template_name = 'garage/vehicle_list.html'
    context_object_name = 'vehicles'
    ordering = ['-id']


class ViewVehicleCreate(MechanicRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'garage/vehicle_form.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get('client_id')
        if client_id:
            initial['client'] = client_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Автомобилът беше добавен успешно!")
        response = super().form_valid(form)
        if 'save_and_add_another' in self.request.POST:
            return redirect(f"{reverse('garage:vehicle_create')}?client_id={self.object.client.id}")
        return response


class ViewVehicleUpdate(MechanicRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'garage/vehicle_form.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, "Данните на автомобила бяха обновени!")
        response = super().form_valid(form)
        if 'save_and_add_another' in self.request.POST:
            return redirect(f"{reverse('garage:vehicle_create')}?client_id={self.object.client.id}")
        return response


class ViewVehicleDelete(ManagerRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'garage/vehicle_delete_confirmation.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def form_valid(self, form):
        messages.warning(self.request, "Автомобилът беше изтрит.")
        return super().form_valid(form)