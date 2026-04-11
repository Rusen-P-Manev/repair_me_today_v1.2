import uuid
from django.core.validators import MinValueValidator
from django.db import models


class PartOrderStatusChoices(models.TextChoices):
    FOR_ORDER = "for_order", "За поръчка"
    ORDERED = "ordered", "Поръчана/и"
    DELIVERED = "delivered", "Доставена/и"


class RepairStatusChoices(models.TextChoices):
    RECEIVED = "received", "За ремонт"
    IN_PROGRESS = "in_progress", "В ремонт"
    COMPLETED = "completed", "Завършен"


class Service(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Име на услугата",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Стойност труд (€)",
    )

    class Meta:
        verbose_name = "Услуга (Ценоразпис)"
        verbose_name_plural = "Услуги (Ценоразпис)"

    def __str__(self):
        return f"{self.name} - {self.price} €."


class RepairJob(models.Model):
    vehicle = models.ForeignKey(
        "garage.Vehicle",
        on_delete=models.CASCADE,
        related_name="repairs",
        verbose_name="Автомобил",
    )

    problem_description = models.TextField(
        verbose_name="Описание на проблема",
    )

    received_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_jobs",
        verbose_name="Приел автомобила",
    )

    repaired_by = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="completed_jobs",
        verbose_name="Извършил ремонта",
    )

    services = models.ManyToManyField(
        "Service",
        through="RepairService",
        blank=True,
        related_name="repair_jobs",
        verbose_name="Извършени услуги",
    )

    status = models.CharField(
        max_length=20,
        choices=RepairStatusChoices.choices,
        default=RepairStatusChoices.RECEIVED,
        verbose_name="Статус на ремонта",
    )

    access_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Код за проследяване",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Създаден на",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последна промяна",
    )

    class Meta:
        verbose_name = "Работна карта"
        verbose_name_plural = "Работни карти"

    def __str__(self):
        return f"Работна карта{self.id} - {self.vehicle.vehicle_registration_number}"


class RepairService(models.Model):
    repair_job = models.ForeignKey(
        "RepairJob",
        on_delete=models.CASCADE,
        verbose_name="Работен картон",
    )

    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        verbose_name="Избрана услуга",
    )

    quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        validators=[MinValueValidator(0.01)],
        verbose_name="Количество / Часове",
    )

    class Meta:
        verbose_name = "Услуга към ремонт"
        verbose_name_plural = "Услуги към ремонти"

    def __str__(self):
        return f"{self.service.name} x {self.quantity}"

class PartOrder(models.Model):
    repair_job = models.ForeignKey(
        "RepairJob",
        on_delete=models.CASCADE,
        related_name="parts",
        verbose_name="Работен картон",
    )

    status = models.CharField(
        max_length=20,
        choices=PartOrderStatusChoices.choices,
        default=PartOrderStatusChoices.FOR_ORDER,
        verbose_name="Статус на частта",
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Описание на частта/частите",
        help_text="Напр. Накладки, Маслен филтър и др."
    )

    invoice_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Номер на доставна фактура",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.01)],
        verbose_name="Цена на частта",
    )

    class Meta:
        verbose_name = "Авточаст към ремонт"
        verbose_name_plural = "Авточасти към ремонти"

    def __str__(self):
        return f"{self.description} - {self.get_status_display()}"


class RepairArchive(models.Model):

    original_job_id = models.IntegerField(
        verbose_name="ID на оригиналния картон"
    )

    vehicle_registration_number = models.CharField(
        max_length=20,
        verbose_name="Рег. номер на автомобила"
    )

    archive_data = models.JSONField(
        verbose_name="JSON Архив на ремонта"
    )

    archived_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата на архивиране"
    )

    class Meta:
        verbose_name = "Архивиран ремонт"
        verbose_name_plural = "Архивирани ремонти"

    def __str__(self):
        return f"Архивиран Картон #{self.original_job_id} - {self.vehicle_registration_number}"