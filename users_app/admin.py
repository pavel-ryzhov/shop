from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users_app.forms import CustomUserCreationForm, CustomUserChangeForm
from users_app.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ["username"]
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (("Additional fields", {"fields": ("phone_number", "is_admin")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional fields", {"fields": ("phone_number", "is_admin")}),)