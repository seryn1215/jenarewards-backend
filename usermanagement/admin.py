from django.contrib import admin

from usermanagement.models import CustomUser


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_center_admin"]


admin.site.register(CustomUser, CustomUserAdmin)
