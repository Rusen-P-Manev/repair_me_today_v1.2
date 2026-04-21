from django.db import models
from common.validators import (
    validate_eik, validate_tax_id,
    validate_iban, validate_vat_number,
)
from common.models import TimeStampModel
from common.mixins import ReadOnlyFieldsModelMixin


class ShopProfile(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Име на сервиза",
    )

    eik = models.CharField(
        max_length=20,
        validators=[validate_eik],
        verbose_name="ЕИК",
    )

    vat_number = models.CharField(
        max_length=20,
        validators=[validate_vat_number],
        verbose_name="ДДС Номер",
    )

    address = models.CharField(
        max_length=200,
        verbose_name="Адрес на сервиза",
    )

    mol = models.CharField(
        max_length=50,
        verbose_name="МОЛ",
    )

    iban = models.CharField(
        max_length=30,
        validators=[validate_iban],
        verbose_name="IBAN",
    )

    class Meta:
        verbose_name = "Профил на сервиза"
        verbose_name_plural = "Профил на сервиза"

    def __str__(self):
        return self.name


class Invoice(ReadOnlyFieldsModelMixin, TimeStampModel):
    readonly_fields = [
        'invoice_number', 'total_amount', 'client_name',
        'tax_id', 'is_corporate', 'repair_job'
    ]

    repair_job = models.OneToOneField(
        "repairs.RepairJob",
        on_delete=models.CASCADE,
        related_name="invoice",
        verbose_name="Работна карта",
    )

    invoice_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Фактура №",
    )

    is_corporate = models.BooleanField(
        default=False,
        verbose_name="Юридическо лице",
    )

    client_name = models.CharField(
        max_length=100,
        verbose_name="Получател (Име/Фирма)",
    )

    tax_id = models.CharField(
        max_length=20,
        validators=[validate_tax_id],
        blank=True,
        null=True,
        verbose_name="ЕИК/ЕГН",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Крайна сума",
    )

    is_paid = models.BooleanField(
        default=False,
        verbose_name="Платена",
    )

    pdf_document = models.FileField(
        upload_to='invoices_pdfs/',
        blank=True,
        null=True,
        verbose_name="PDF Документ"
    )

    @classmethod
    def _generate_invoice_number(cls):
        invoices = cls.objects.filter(invoice_number__startswith='INV-')

        max_num = 0
        for inv in invoices:
            try:
                current_num = int(inv.invoice_number.split('-')[1])
                if current_num > max_num:
                    max_num = current_num
            except (IndexError, ValueError):
                continue
        return f"INV-{max_num + 1:06d}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.invoice_number = self._generate_invoice_number()

        super().save(*args, **kwargs)

        if self.is_paid:
            from common.utils import create_repair_archive
            from repairs.models import RepairArchive

            if not RepairArchive.objects.filter(original_job_id=self.repair_job.id).exists():
                create_repair_archive(self.repair_job)