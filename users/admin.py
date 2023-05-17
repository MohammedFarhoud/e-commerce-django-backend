from django.contrib import admin
from users.models import Address, CustomUser
from django.contrib.auth.admin import UserAdmin


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [AddressInline]

    add_fieldsets  = (
        (None, {'fields': ('username', 'password', 'confirm_password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
