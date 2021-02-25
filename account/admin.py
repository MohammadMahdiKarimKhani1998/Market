from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserForm, CustomUserChangeForm
from .models import User, Address, UserEmail, Shop
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'mobile', 'image', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('allay', 'city', 'street', 'zip_code')
    list_filter = ('city', 'zip_code')
    search_fields = ('zip_code', )
    date_hierarchy = 'updated_at'


@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ('email_to', 'subject')
    list_filter = ('email_to', )
    search_fields = ('email_to', )
    date_hierarchy = 'updated_at'


@admin.register(Shop)
class ShopUser(admin.ModelAdmin):
    list_display = ('slug', 'name', 'created_at')
    list_filter = ('slug', 'name')
    search_fields = ('slug', 'name')
    date_hierarchy = 'updated_at'


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
