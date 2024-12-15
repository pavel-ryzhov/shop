from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import BooleanField

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(null=False, unique=True, blank=False)
    is_admin = BooleanField(default=False)
    @staticmethod
    def get_absolute_url():
        return reverse("manage_users")
