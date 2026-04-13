from django.db import models
from django.contrib.auth.models import AbstractUser


class CarServiceUsers(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Имейл адрес"
    )

    class Meta:
        verbose_name = "Потребител"
        verbose_name_plural = "Потребители"

    def __str__(self):
        return self.username
