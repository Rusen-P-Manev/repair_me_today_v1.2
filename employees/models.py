from django.db import models
from django.conf import settings
from common.validators import validate_name_letters_only, validate_phone_number

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employee_profile",
        verbose_name="Потребителски акаунт"
    )

    first_name = models.CharField(
        max_length=50,
        verbose_name="Име",
    )

    last_name = models.CharField(
        max_length=50,
        validators=[validate_name_letters_only],
        verbose_name="Фамилия",
    )

    position = models.CharField(
        max_length=50,
        validators=[validate_name_letters_only],
        verbose_name="Длъжност",
    )

    phone_number = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        blank=True,
        null=True,
        verbose_name="Телефонен номер",
    )

    qualifications = models.ManyToManyField(
        'repairs.Service',
        blank=True,
        related_name='qualified_mechanics',
        verbose_name="Квалификация"
    )

    class Meta:
        verbose_name = "Служител"
        verbose_name_plural = "Служители"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"