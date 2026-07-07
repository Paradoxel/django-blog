import re

from django.core.exceptions import ValidationError


IRAN_MOBILE_REGEX = re.compile(
    r"^(09\d{9}|\+989\d{9})$"
)


def validate_iran_phone_number(value):
    """
    Validate Iranian mobile numbers.

    Accepted formats:
    - 09xxxxxxxxx
    - +989xxxxxxxxx
    """

    if value and not IRAN_MOBILE_REGEX.fullmatch(value):
        raise ValidationError(
            "Enter a valid Iranian mobile number."
        )