from django.test import TestCase
from repairs.models import Service, RepairJob, PartOrder
from garage.models import Client, Vehicle


class RepairsModelsTests(TestCase):

    def setUp(self):
        self.service = Service.objects.create(
            name="Смяна на масло",
            price=50.00
        )

        self.client = Client.objects.create(
            first_name="Тест",
            last_name="Тестов",
            phone_number="0888123456"
        )

        self.vehicle = Vehicle.objects.create(
            client=self.client,
            make="Audi",
            model="A4",
            year=2010,
            vin="WAUZZZ00000000123",
            vehicle_registration_number="B1234BB"
        )
        self.repair = RepairJob.objects.create(
            vehicle=self.vehicle,
            problem_description="Тропане",
            status="received"
        )

    def test_service_string_representation(self):
        self.assertEqual(str(self.service), "Смяна на масло - 50.0 €.")

    def test_repair_job_default_status(self):
        self.assertEqual(self.repair.status, "received")

    def test_part_order_creation(self):
        part = PartOrder.objects.create(
            repair_job=self.repair,
            description="Носач",
            price=150.00,
            status="for_order"
        )
        self.assertEqual(str(part), "Носач - За поръчка")
        self.assertEqual(part.repair_job, self.repair)