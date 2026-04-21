from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Създаден на"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последна промяна"
    )

    class Meta:
        abstract = True