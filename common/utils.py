from repairs.models import RepairArchive
from decimal import Decimal


def calculate_vat(total_amount):
    total = Decimal(str(total_amount)) if total_amount else Decimal('0.00')
    subtotal = total / Decimal('1.20')
    vat = total - subtotal

    return {
        'subtotal': round(subtotal, 2),
        'vat': round(vat, 2)
    }



def create_repair_archive(job):
    parts_data = []
    for part in job.parts.all():
        parts_data.append({
            'description': part.description,
            'status': part.get_status_display(),
            'price': str(part.price) if part.price else "0.00"
        })

    services_data = []
    for rs in job.repairservice_set.all():
        services_data.append({
            'name': rs.service.name,
            'quantity': str(rs.quantity),
            'price_per_unit': str(rs.service.price),
            'total_service_price': str(rs.quantity * rs.service.price)
        })

    json_payload = {
        'job_info': {
            'problem_description': job.problem_description,
            'received_by': job.received_by.first_name + " " + job.received_by.last_name if job.received_by else "Няма данни",
        },
        'vehicle_info': {
            'registration': job.vehicle.vehicle_registration_number,
            'make': job.vehicle.make,
            'model': job.vehicle.model,
            'vin': job.vehicle.vin,
            'year': job.vehicle.year,
        },
        'client_info': {
            'name': job.invoice.client_name,
            'tax_id': job.invoice.tax_id,
            'phone': job.vehicle.client.phone_number,
        },
        'parts': parts_data,
        'services': services_data,
        'invoice_info': {
            'invoice_number': job.invoice.invoice_number,
            'total_amount': str(job.invoice.total_amount),
            'paid_on': str(job.invoice.created_at)
        }
    }

    RepairArchive.objects.create(
        original_job_id=job.id,
        vehicle_registration_number=job.vehicle.vehicle_registration_number,
        archive_data=json_payload
    )


def check_if_ready_for_invoicing(job):
    from repairs.models import RepairStatusChoices, PartOrderStatusChoices

    if job.status != RepairStatusChoices.COMPLETED:
        return False

    for part in job.parts.all():
        if part.status != PartOrderStatusChoices.DELIVERED or not part.price:
            return False

    if not job.parts.exists() and not job.repairservice_set.exists():
        return False
    return True