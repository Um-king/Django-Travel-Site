# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'username', 'nickname', 'is_staff', ]  # 여기에 원하는 필드 추가
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('nickname', 'profile_image',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
