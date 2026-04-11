from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from invoicing.models import ShopProfile
from common.utils import calculate_vat
from .models import (
    RepairJob, PartOrder, Service,
    RepairArchive, RepairService
)
from .forms import (
    RepairJobCreateForm, RepairJobUpdateForm, PartOrderForm,
    PublicClientInfoForm, ServiceCatalogForm, RepairServiceForm
)

 # repairs -->
class ViewRepairJobList(ListView):
    model = RepairJob
    template_name = 'repairs/job_list.html'
    context_object_name = 'jobs'
    ordering = ['-created_at']


class ViewRepairJobDetail(DetailView):
    model = RepairJob
    template_name = 'repairs/job_detail.html'
    context_object_name = 'job'


class ViewRepairJobCreate(CreateView):
    model = RepairJob
    form_class = RepairJobCreateForm
    template_name = 'repairs/job_form.html'

    def get_success_url(self):
        return reverse('repairs:job_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Работният картон беше отворен успешно!")
        return super().form_valid(form)


class ViewRepairJobUpdate(UpdateView):
    model = RepairJob
    form_class = RepairJobUpdateForm
    template_name = 'repairs/job_form.html'

    def get_success_url(self):
        return reverse('repairs:job_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Статусът на ремонта беше обновен!")
        return super().form_valid(form)


class ViewRepairJobDelete(DeleteView):
    model = RepairJob
    template_name = 'repairs/job_delete_confirmation.html'
    success_url = reverse_lazy('repairs:job_list')

    def form_valid(self, form):
        messages.warning(self.request, "Работният картон беше изтрит завинаги.")
        return super().form_valid(form)


# parts -->
class ViewPartOrderCreate(CreateView):
    model = PartOrder
    form_class = PartOrderForm
    template_name = 'repairs/add_part_form.html'

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        repair_job = get_object_or_404(RepairJob, pk=job_id)

        form.instance.repair_job = repair_job

        messages.success(self.request, "Авточастта беше добавена към ремонта!")
        response = super().form_valid(form)

        if 'save_and_add_another' in self.request.POST:
            return redirect('repairs:part_create', job_id=job_id)

        return response

    def get_success_url(self):
        return reverse('repairs:job_detail', kwargs={'pk': self.kwargs.get('job_id')})


class ViewPartOrderDelete(DeleteView):
    model = PartOrder
    template_name = 'repairs/part_delete_confirmation.html'

    def get_success_url(self):
        return reverse('repairs:job_detail', kwargs={'pk': self.object.repair_job.pk})

    def form_valid(self, form):
        messages.warning(self.request, "Частта беше премахната от списъка.")
        return super().form_valid(form)


# public client info --?
class ViewClientInfo(View):
    template_name = 'repairs/public_client_info.html'

    def get(self, request):
        form = PublicClientInfoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PublicClientInfoForm(request.POST)
        job = None

        if form.is_valid():
            token_value = form.cleaned_data['tracking_code']
            reg_number = form.cleaned_data['vehicle_registration_number']

            job = RepairJob.objects.filter(
                access_token=token_value,
                vehicle__vehicle_registration_number__iexact=reg_number
            ).first()

            if not job:
                messages.error(request, "Не е открит ремонт с тези данни. Моля, проверете въведената информация.")

        return render(request, self.template_name, {'form': form, 'job': job})

# repairs --->
class ViewRepairServiceCreate(CreateView):
    model = RepairService
    form_class = RepairServiceForm
    template_name = 'repairs/add_service_form.html'

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        repair_job = get_object_or_404(RepairJob, pk=job_id)
        form.instance.repair_job = repair_job

        messages.success(self.request, "Услугата беше добавена към ремонта!")
        response = super().form_valid(form)

        if 'save_and_add_another' in self.request.POST:
            return redirect('repairs:service_create', job_id=job_id)

        return response

    def get_success_url(self):
        return reverse('repairs:job_detail', kwargs={'pk': self.kwargs.get('job_id')})


class ViewRepairServiceDelete(DeleteView):
    model = RepairService
    template_name = 'repairs/service_delete_confirmation.html'

    def get_success_url(self):
        return reverse('repairs:job_detail', kwargs={'pk': self.object.repair_job.pk})

    def form_valid(self, form):
        messages.warning(self.request, "Услугата беше премахната от списъка.")
        return super().form_valid(form)


# catalog views -->
class ViewServiceCatalogList(ListView):
    model = Service
    template_name = 'repairs/catalog_list.html'
    context_object_name = 'services'
    ordering = ['name']


class ViewServiceCatalogCreate(CreateView):
    model = Service
    form_class = ServiceCatalogForm
    template_name = 'repairs/catalog_form.html'
    success_url = reverse_lazy('repairs:service_catalog_list')

    def form_valid(self, form):
        messages.success(self.request, "Услугата беше добавена в каталога!")
        response = super().form_valid(form)

        if 'save_and_add_another' in self.request.POST:
            return redirect(self.request.path)

        return response

class ViewServiceCatalogUpdate(UpdateView):
    model = Service
    form_class = ServiceCatalogForm
    template_name = 'repairs/catalog_form.html'
    success_url = reverse_lazy('repairs:service_catalog_list')

    def form_valid(self, form):
        messages.success(self.request, "Услугата беше обновена успешно!")
        return super().form_valid(form)

class ViewServiceCatalogDelete(DeleteView):
    model = Service
    template_name = 'repairs/catalog_delete_confirmation.html'
    success_url = reverse_lazy('repairs:service_catalog_list')

    def form_valid(self, form):
        messages.warning(self.request, "Услугата беше изтрита от каталога.")
        return super().form_valid(form)


class ViewRepairArchiveList(ListView):
    model = RepairArchive
    template_name = 'repairs/archive_list.html'
    context_object_name = 'archives'
    ordering = ['-id']


class ViewArchivedInvoiceDetail(DetailView):
    model = RepairArchive
    template_name = 'repairs/archived_invoice_detail.html'
    context_object_name = 'archive'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archive_data = self.object.archive_data

        context['shop_profile'] = ShopProfile.objects.first()

        total_amount = archive_data.get('invoice_info', {}).get('total_amount', 0)
        vat_data = calculate_vat(total_amount)

        context['subtotal'] = vat_data['subtotal']
        context['vat'] = vat_data['vat']
        context['total_amount'] = total_amount

        return context