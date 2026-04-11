from django import forms
from .models import Invoice
from common.mixins import BootstrapFormMixin


class InvoiceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'is_corporate', 'client_name', 'tax_id', 'total_amount', 'is_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['client_name'].disabled = True
        self.fields['client_name'].required = False

        self.fields['tax_id'].disabled = True
        self.fields['tax_id'].required = False

        self.fields['total_amount'].disabled = True
        self.fields['total_amount'].required = False

        self.fields['is_corporate'].disabled = True
        self.fields['is_corporate'].required = False

        self.fields['invoice_number'].widget.attrs['placeholder'] = 'напр. 0000000123'