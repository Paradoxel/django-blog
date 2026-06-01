import re

from django.core.exceptions import ValidationError

IRAN_PHONE_REGEX = re.compile(r"^(09\d{9}|\+989\d{9})$")


def validate_iran_phone_number(value):
    if value and not IRAN_PHONE_REGEX.match(value):
        raise ValidationError("Enter a valid Iranian mobile number.")
