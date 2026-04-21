from celery import shared_task
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML
from .models import Invoice, ShopProfile
from common.utils import calculate_vat


@shared_task
def generate_invoice_pdf(invoice_id):

    invoice = Invoice.objects.get(id=invoice_id)
    shop_profile = ShopProfile.objects.first()
    vat_data = calculate_vat(invoice.total_amount)

    context = {
        'invoice': invoice,
        'shop_profile': shop_profile,
        'subtotal': vat_data['subtotal'],
        'vat': vat_data['vat'],
    }

    html_string = render_to_string('invoicing/invoice_detail.html', context)

    html = HTML(string=html_string, base_url='http://127.0.0.1:8000')  # base_url помага за зареждане на CSS/снимки
    pdf_bytes = html.write_pdf()

    file_name = f"{invoice.invoice_number}.pdf"
    invoice.pdf_document.save(file_name, ContentFile(pdf_bytes))

    return f"Успешно генерирахте фактура {invoice.invoice_number}"