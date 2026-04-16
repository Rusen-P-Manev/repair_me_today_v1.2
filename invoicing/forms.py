from django import forms
from .models import Invoice
from common.mixins import BootstrapFormMixin


class InvoiceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['is_corporate', 'client_name', 'tax_id', 'total_amount', 'is_paid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        readonly_text_fields = ['client_name', 'tax_id', 'total_amount']

        for field in readonly_text_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].required = False
            existing_classes = self.fields[field].widget.attrs.get('class', '')
            self.fields[field].widget.attrs['class'] = f"{existing_classes} form-control-plaintext".strip()

        self.fields['is_corporate'].disabled = True
        self.fields['is_corporate'].required = False

        