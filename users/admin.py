from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username','last_login', 'bio', 'social_handle', 'is_staff', 'is_active')
    list_filter = ('email', 'username', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email','username','avatar','bio','social_handle', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('email', 'social_handle', 'username', 'avatar', 'password1', 'password2','social_handle', 'is_staff', 'is_active')
        }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)