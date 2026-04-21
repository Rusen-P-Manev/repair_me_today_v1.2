from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from garage.models import Client
from .models import CarServiceUsers
from common.mixins import BootstrapFormMixin


class ClientRegistrationForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        label="Име",
        required=True
    )
    last_name = forms.CharField(
        max_length=50,
        label="Фамилия",
        required=True
    )
    phone_number = forms.CharField(
        max_length=20,
        label="Телефон",
        required=True
    )
    email = forms.EmailField(
        label="Имейл",
        required=True
    )


    class Meta(UserCreationForm.Meta):
        model = CarServiceUsers
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            Client.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email']
            )
        return user