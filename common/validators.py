import re
import datetime
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


def validate_vin(value):

    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', value):
        raise ValidationError("Невалиден VIN номер! Трябва да е 17 символа (главни букви и цифри) и без I, O и Q.")

def validate_eik(value):
    if not re.match(r'^\d{9}$|^\d{13}$', value):
        raise ValidationError("ЕИК/Булстат трябва да съдържа точно 9 или 13 цифри.")

def validate_tax_id(value):
    if not re.match(r'^(\d{9}|\d{10}|\d{13})$', value):
        raise ValidationError("Невалиден формат. ЕИК трябва да е 9 или 13 цифри, а ЕГН - 10 цифри.")

def validate_phone_number(value):
    if not re.match(r'^(?:\+359|0)[1-9]\d{7,8}$', value):
        raise ValidationError("Невалиден формат на телефонен номер. Използвайте 08... или +359...")

def validate_year(value):
    current_year = datetime.date.today().year
    if value < 1900 or value > current_year:
        raise ValidationError(f"Годината трябва да бъде между 1900 и {current_year}.")

def validate_name_letters_only(value):

    if not re.match(r'^[A-Za-zА-Яа-я]+$', value):
        raise ValidationError("Полето може да съдържа само малки и големи букви букви.")

def validate_iban(value):

    if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$', value):
        raise ValidationError("Невалиден формат на IBAN")

def validate_vat_number(value):
    if not re.match(r'^BG\d{9,10}$', value):
        raise ValidationError("ДДС номерът трябва да започва с 'BG' последван от 9 или 10 цифри.")

custom_email_validator = EmailValidator(
    message="Моля, въведете валиден имейл адрес (name@domain.com)."
)