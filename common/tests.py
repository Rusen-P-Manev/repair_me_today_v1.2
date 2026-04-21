from django.test import TestCase
from django.core.exceptions import ValidationError
from common.validators import (
    validate_vin, validate_phone_number, validate_year,
    validate_name_letters_only, validate_eik
)

class CustomValidatorsTests(TestCase):

    def test_validate_vin_valid(self):
        self.assertIsNone(validate_vin('WBAJS31000DEM0123'))

    def test_validate_vin_invalid_short(self):
        with self.assertRaises(ValidationError):
            validate_vin('WBAJS310')

    def test_validate_vin_invalid_long(self):
        with self.assertRaises(ValidationError):
            validate_vin('WBAJS31000DEMO123456789')

    def test_validate_phone_number_valid(self):
        self.assertIsNone(validate_phone_number('0888123456'))
        self.assertIsNone(validate_phone_number('+359888123456'))

    def test_validate_phone_number_invalid_letters(self):
        with self.assertRaises(ValidationError):
            validate_phone_number('088812345a')

    def test_validate_year_valid(self):
        self.assertIsNone(validate_year(2015))
        self.assertIsNone(validate_year(1990))

    def test_validate_year_invalid_future(self):
        with self.assertRaises(ValidationError):
            validate_year(2050)

    def test_validate_year_invalid_too_old(self):
        with self.assertRaises(ValidationError):
            validate_year(1850)

    def test_validate_name_letters_only_valid(self):
        self.assertIsNone(validate_name_letters_only('Иван'))
        self.assertIsNone(validate_name_letters_only('Ivan'))

    def test_validate_name_letters_only_invalid(self):
        with self.assertRaises(ValidationError):
            validate_name_letters_only('Иван123')

    def test_validate_eik_valid(self):
        self.assertIsNone(validate_eik('123456789'))
        self.assertIsNone(validate_eik('1234567890123'))

    def test_validate_eik_invalid(self):
        with self.assertRaises(ValidationError):
            validate_eik('12345678')