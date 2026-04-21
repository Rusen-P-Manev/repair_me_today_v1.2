from django import forms
from common.mixins import BootstrapFormMixin
from .models import (
    RepairJob, PartOrder, PartOrderStatusChoices,
    Service, RepairService
)

# repairjob -->
class RepairJobCreateForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = RepairJob
        fields = ['vehicle', 'problem_description', 'received_by']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'received_by': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'problem_description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Опишете подробно оплакванията на клиента...'}),
        }


class RepairJobUpdateForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = RepairJob
        fields = ['vehicle', 'problem_description', 'status', 'received_by', 'repaired_by']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'status': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'received_by': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'repaired_by': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'problem_description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].disabled = True


# parst -->

class PartOrderForm(forms.ModelForm):
    class Meta:
        model = PartOrder
        fields = ['description', 'status', 'invoice_number', 'price']
        widgets = {
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Напр. Накладки, Маслен филтър и др.'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        price = cleaned_data.get('price')

        if status == PartOrderStatusChoices.DELIVERED and not price:
            self.add_error('price', 'Моля, въведете цена!')

        return cleaned_data


class PublicClientInfoForm(BootstrapFormMixin, forms.Form):
    tracking_code = forms.UUIDField(
        label="Код за проследяване (UUID)",
        widget=forms.TextInput(attrs={'placeholder': 'напр. 123e4567-e89b-12d3-a456-426614174000'})
    )

    vehicle_registration_number = forms.CharField(
        label="Регистрационен номер",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'напр. СВ1234АВ'})
    )



class RepairServiceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RepairService
        fields = ['service', 'quantity']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'step': '0.1'}),
        }
        labels = {
            'service': 'Изберете услуга',
            'quantity': 'Количество / Часове'
        }


class ServiceCatalogForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'напр. Смяна на масло, Диагностика и др.'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }