from django.contrib import admin
from .models import User
from .models.profiles import Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "username",
        "id",
        "email",
        "is_active",
        "is_superuser",
        "is_verified",
    ]
    fieldsets = (
        (
            "authentication",
            {
                "fields": ("username", "email", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_active", "is_superuser", "is_verified"),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = [
        "user__username",
        "user__email",
        "first_name",
        "last_name",
        "country",
        "phone",
    ]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
