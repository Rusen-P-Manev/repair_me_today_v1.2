from django.test import TestCase
from garage.models import Client, Vehicle

class GarageModelsTests(TestCase):

    def setUp(self):
        self.client = Client.objects.create(
            first_name="Иван",
            last_name="Иванов",
            phone_number="0888123456",
            address_city="София",
            address_street="ул. Дълбока дупка 1"
        )
        self.vehicle = Vehicle.objects.create(
            client=self.client,
            make="BMW",
            model="X5",
            year=2015,
            vin="WBAX5000000000123",
            vehicle_registration_number="CB1234XX"
        )

    def test_client_creation_success(self):
        self.assertEqual(self.client.first_name, "Иван")
        self.assertEqual(self.client.phone_number, "0888123456")

    def test_client_string_representation(self):
        self.assertEqual(str(self.client), "Иван Иванов")

    def test_corporate_client_string_representation(self):
        corp_client = Client.objects.create(
            is_corporate=True,
            company_name="Бръм Бръм ООД",
            tax_id="123456789",
            first_name="Петър",
            last_name="Петров",
            phone_number="0899000000"
        )
        self.assertEqual(str(corp_client), "Бръм Бръм ООД (123456789)")

    def test_vehicle_creation_success(self):
        self.assertEqual(self.vehicle.make, "BMW")
        self.assertEqual(self.vehicle.client, self.client)

    def test_vehicle_string_representation(self):
        expected_str = "CB1234XX - BMW X5"
        self.assertEqual(str(self.vehicle), expected_str)