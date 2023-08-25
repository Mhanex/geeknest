#PASSWORD VALIDTOR IN OTHER TO OVERRIDE DJANGO DEFAULT PASSWORD VALIDATOR
from django.core.exceptions import ValidationError
import re

def validate_alphanumeric_password(value):
    if not re.match(r'^(?=.*[a-zA-Z])(?=.*\d)', value):
        raise ValidationError("Password must contain both letters and digits.")

