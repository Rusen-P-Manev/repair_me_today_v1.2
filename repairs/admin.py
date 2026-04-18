from django.contrib import admin
from .models import RepairJob, Service, RepairService, PartOrder


class RepairServiceInline(admin.TabularInline):
    model = RepairService
    extra = 1


class PartOrderInline(admin.TabularInline):
    model = PartOrder
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
    )


@admin.register(RepairJob)
class RepairJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vehicle",
        "status",
        "access_token",
    )

    inlines = (
        RepairServiceInline,
        PartOrderInline,
    )

    readonly_fields = (
        "access_token",
        "created_at",
        "updated_at",
    )