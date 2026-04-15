from django.shortcuts import render
from decimal import Decimal
from .models import Invoice, ShopProfile
from django.views import View
from .forms import InvoiceForm
from django.contrib import messages
from repairs.models import RepairJob
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from common.utils import create_repair_archive, calculate_vat, check_if_ready_for_invoicing


class ViewInvoiceList(ListView):
    model = Invoice
    template_name = 'invoicing/invoice_list.html'
    context_object_name = 'invoices'
    ordering = ['-created_at']


class ViewInvoiceCreate(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoicing/invoice_form.html'

    @staticmethod
    def _validate_invoicing_requisites(job):
        if hasattr(job, 'invoice'):
            return True, "Вече има издадена фактура!"

        if not check_if_ready_for_invoicing(job):
            return True, "Ремонтът не може да бъде фактуриран!"
        return False, ""

    def dispatch(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(RepairJob, pk=job_id)

        has_error, error_msg = self._validate_invoicing_requisites(job)

        if has_error:
            messages.error(self.request, error_msg)
            return redirect('repairs:job_detail', pk=job.id)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(RepairJob, pk=job_id)
        client = job.vehicle.client

        initial['is_corporate'] = client.is_corporate
        if client.is_corporate:
            initial['client_name'] = client.company_name
            initial['tax_id'] = client.tax_id
        else:
            initial['client_name'] = f"{client.first_name} {client.last_name}"
        initial['tax_id'] = client.tax_id if client.tax_id else ""

        total = Decimal('0.00')

        for rs in job.repairservice_set.all():
            total += rs.service.price * rs.quantity

        for part in job.parts.all():
            if part.price:
                total += part.price

        total_with_vat = total * Decimal('1.20')
        initial['total_amount'] = round(total_with_vat, 2)

        return initial

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(RepairJob, pk=job_id)

        form.instance.repair_job = job

        initial_data = self.get_initial()
        form.instance.total_amount = initial_data['total_amount']
        form.instance.client_name = initial_data['client_name']
        form.instance.tax_id = initial_data['tax_id']
        form.instance.is_corporate = initial_data['is_corporate']

        messages.success(self.request, "Фактурата беше генерирана успешно!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('invoicing:invoice_detail', kwargs={'pk': self.object.pk})


class ViewInvoiceDetail(DetailView):
    model = Invoice
    template_name = 'invoicing/invoice_detail.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_profile'] = ShopProfile.objects.first()

        total = float(self.object.total_amount or 0)
        subtotal = total / 1.20
        vat = total - subtotal

        vat_data = calculate_vat(self.object.total_amount)
        context['subtotal'] = vat_data['subtotal']
        context['vat'] = vat_data['vat']

        return context


class ViewInvoiceMarkPaid(View):

    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)

        if not invoice.is_paid:
            invoice.is_paid = True
            invoice.save()

            create_repair_archive(invoice.repair_job)

            messages.success(request, "Фактурата е платена! Данните са архивирани.")
        else:
            messages.warning(request, "Тази фактура вече е платена.")

        return redirect('invoicing:invoice_detail', pk=invoice.pk)