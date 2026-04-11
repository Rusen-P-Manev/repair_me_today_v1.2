from django.contrib import admin
from .models import Client, Vehicle


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "is_corporate",
        "company_name",
        "phone_number",
    )

    list_filter = (
        "is_corporate",
    )

    search_fields = (
        "first_name",
        "last_name",
        "company_name",
        "tax_id",
        "phone_number",
    )


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_registration_number",
        "make",
        "model",
        "client",
    )

    search_fields = (
        "vehicle_registration_number",
        "vin",
    )