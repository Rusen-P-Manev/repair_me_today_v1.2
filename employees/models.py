from django.db import models
from common.validators import validate_name_letters_only


class Employee(models.Model):
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

    class Meta:
        verbose_name = "Служител"
        verbose_name_plural = "Служители"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"