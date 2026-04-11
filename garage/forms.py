from django import forms
from .models import Client, Vehicle
from common.mixins import BootstrapFormMixin


class ClientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'is_corporate', 'company_name', 'tax_id',
            'first_name', 'last_name', 'phone_number', 'email',
            'address_city', 'address_street', 'address_zip'
        ]

    def clean_first_name(self):
        return self.cleaned_data.get('first_name', '').strip().capitalize()

    def clean_last_name(self):
        return self.cleaned_data.get('last_name', '').strip().capitalize()

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        return phone.replace(" ", "")

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id')
        if tax_id:
            return tax_id.replace(" ", "")
        return tax_id

    def clean(self):
        cleaned_data = super().clean()
        is_corporate = cleaned_data.get('is_corporate')
        company_name = cleaned_data.get('company_name')
        tax_id = cleaned_data.get('tax_id')

        if is_corporate:
            if not company_name:
                self.add_error('company_name', 'Това поле е задължително за юридически лица.')
            if not tax_id:
                self.add_error('tax_id', 'Това поле е задължително за юридически лица.')
        else:
            cleaned_data['company_name'] = None
            cleaned_data['tax_id'] = None

        return cleaned_data


class VehicleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['client', 'vehicle_registration_number', 'make', 'model', 'year', 'vin']

        widgets = {
            'client': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }

    def clean_vehicle_registration_number(self):
        reg_num = self.cleaned_data.get('vehicle_registration_number', '')
        return reg_num.replace(" ", "").upper()

    def clean_vin(self):
        vin = self.cleaned_data.get('vin', '')
        return vin.replace(" ", "").upper()

    def clean_make(self):
        return self.cleaned_data.get('make', '').strip().capitalize()

    def clean_model(self):
        return self.cleaned_data.get('model', '').strip().capitalize()