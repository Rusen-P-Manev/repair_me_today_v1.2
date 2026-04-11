from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client, Vehicle
from .forms import ClientForm, VehicleForm

# clients -->
class ViewClientList(ListView):
    model = Client
    template_name = 'garage/client_list.html'
    context_object_name = 'clients'
    ordering = ['-id']

class ViewClientCreate(CreateView):
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

class ViewClientUpdate(UpdateView):
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

class ViewClientDelete(DeleteView):
    model = Client
    template_name = 'garage/client_delete_confirmation.html'
    success_url = reverse_lazy('garage:client_list')

    def form_valid(self, form):
        messages.warning(self.request, "Клиентът беше изтрит от системата.")
        return super().form_valid(form)


# vehicles -->
class ViewVehicleList(ListView):
    model = Vehicle
    template_name = 'garage/vehicle_list.html'
    context_object_name = 'vehicles'
    ordering = ['-id']

class ViewVehicleCreate(CreateView):
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

class ViewVehicleUpdate(UpdateView):
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

class ViewVehicleDelete(DeleteView):
    model = Vehicle
    template_name = 'garage/vehicle_delete_confirmation.html'
    success_url = reverse_lazy('garage:vehicle_list')

    def form_valid(self, form):
        messages.warning(self.request, "Автомобилът беше изтрит.")
        return super().form_valid(form)