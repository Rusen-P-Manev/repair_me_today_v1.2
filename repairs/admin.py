from django.contrib import admin
from .models import RepairJob, Service, RepairService, PartOrder, RepairArchive


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


@admin.register(RepairArchive)
class RepairArchiveAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "original_job_id",
        "vehicle_registration_number",
        "created_at",
    )

    search_fields = (
        "original_job_id",
        "vehicle_registration_number",
    )

    readonly_fields = (
        "original_job_id",
        "vehicle_registration_number",
        "archive_data",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False