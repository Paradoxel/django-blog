import re

from django.core.exceptions import ValidationError


# Valid formats: 09xxxxxxxxx (local) or +989xxxxxxxxx (international)
IRAN_PHONE_REGEX = re.compile(r"^(09\d{9}|\+989\d{9})$")


def validate_iran_phone_number(value):
    """Validate Iranian mobile number. Skips if empty (field is optional)."""
    if value and not IRAN_PHONE_REGEX.match(value):
        raise ValidationError("Enter a valid Iranian mobile number.")