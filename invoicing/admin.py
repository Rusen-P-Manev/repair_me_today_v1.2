from django.contrib import admin
from .models import Invoice, ShopProfile


@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "eik",
        "mol",
        "vat_number",
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "client_name",
        "total_amount",
        "is_paid",
        "created_at",
    )

    list_filter = (
        "is_paid",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "client_name",
        "tax_id",
    )

    readonly_fields = (
        "created_at",
    )