from django.contrib import admin
from users.models import Address, CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser)
admin.site.register(Address)