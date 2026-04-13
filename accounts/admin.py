from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CarServiceUsers

@admin.register(CarServiceUsers)
class CarServiceUsersAdmin(UserAdmin):
    pass
