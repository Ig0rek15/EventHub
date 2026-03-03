from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, AuthIdentity


class AuthIdentityInline(admin.TabularInline):
    model = AuthIdentity
    extra = 0
    readonly_fields = ('provider', 'provider_user_id', 'created_at')
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = (
        'id',
        'email',
        'is_staff',
        'is_active',
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    readonly_fields = ('last_login',)
    inlines = (AuthIdentityInline,)


@admin.register(AuthIdentity)
class AuthIdentityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'provider',
        'provider_user_id',
        'created_at',
    )
    search_fields = ('provider_user_id',)
    list_filter = ('provider',)
    readonly_fields = ('created_at',)
