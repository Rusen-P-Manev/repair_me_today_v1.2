from django.db import models
from common.validators import (
    validate_tax_id, validate_phone_number, validate_vin,
    custom_email_validator, validate_year, validate_name_letters_only,
)


class Client(models.Model):
    is_corporate = models.BooleanField(
        default=False,
        verbose_name="Юридическо лице",
    )

    company_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Име на юридическо лице",
    )

    tax_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[validate_tax_id],
        verbose_name="ЕИК/Булстат",
    )

    address_city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Град",
    )

    address_street = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Улица и №",
    )

    address_zip = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Пощенски код",
    )

    first_name = models.CharField(
        max_length=50,
        validators=[validate_name_letters_only],
        verbose_name="Име / МОЛ",
    )

    last_name = models.CharField(
        max_length=50,
        validators=[validate_name_letters_only],
        verbose_name="Фамилия",
    )

    phone_number = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        verbose_name="Телефон",
    )

    email = models.EmailField(
        blank=True,
        null=True,
        validators=[custom_email_validator],
        verbose_name="Имейл",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенти"

    def __str__(self):
        if self.is_corporate and self.company_name:
            return f"{self.company_name} ({self.tax_id})"
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="vehicles",
        verbose_name="Клиент",
    )

    vehicle_registration_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Регистрационен номер",
    )

    make = models.CharField(
        max_length=50,
        verbose_name="Марка",
    )

    model = models.CharField(
        max_length=50,
        verbose_name="Модел",
    )

    year = models.PositiveIntegerField(
        validators=[validate_year],
        verbose_name="Година на производство",

    )

    vin = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_vin],
        verbose_name="VIN номер",
    )

    class Meta:
        verbose_name = "Автомобил"
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.vehicle_registration_number} - {self.make} {self.model}"