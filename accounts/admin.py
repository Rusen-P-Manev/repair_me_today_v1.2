from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm
from .models import CarServiceUsers

class CarServiceUserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = CarServiceUsers
        fields = AdminUserCreationForm.Meta.fields + ('email',)

@admin.register(CarServiceUsers)
class CarServiceUsersAdmin(UserAdmin):
    add_form = CarServiceUserCreationForm

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Допълнителна информация', {
            'fields': ('email',),
        }),
    )