from collections import OrderedDict
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from usermanagement.forms import CenterAdminForm, UserWithProfileForm
from .models import (
    CenterAdmin,
    CenterAdminPermissionHelper,
    CustomUser,
    User,
    UserProfile,
)
from django.contrib.auth.models import Group

from .models import CustomUser

from django import forms


class CenterAdminModelAdmin(ModelAdmin):
    model = CenterAdmin
    permission_helper_class = CenterAdminPermissionHelper
    menu_label = "Center Admins"

    menu_icon = "tag"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("username", "email", "last_login", "date_joined")

    form_fields_exclude = (
        "user_permissions",
        "last_login",
        "is_superuser",
        "date_joined",
        "is_staff",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_center_admin=True)


modeladmin_register(CenterAdminModelAdmin)


class UserModelAdmin(ModelAdmin):
    model = User
    menu_label = "Users"
    menu_icon = "user"
    menu_order = 300

    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("uid", "username", "email", "last_login", "date_joined")
    form_fields_exclude = (
        "user_permissions",
        "groups",
        "is_center_admin",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_center_admin=False, is_staff=False, is_superuser=False)


# modeladmin_register(UserModelAdmin)


class UserProfileAdmin(ModelAdmin):
    model = UserProfile
    menu_label = "Users"
    form = UserWithProfileForm

    menu_icon = (
        "user"  # Used for the menu icon, can also use any of the FontAwesome icons
    )
    menu_order = 200  # Determines where in the menu to place this item
    add_to_settings_menu = False  # Whether to add this model to the settings submenu
    exclude_from_explorer = (
        False  # Whether to exclude this model from the explorer menu
    )
    form_fields_exclude = ("coins",)
    list_display = ("user", "calculated_coins")
    search_fields = ("user__username",)

    def get_form_class(self, request, instance=None, **kwargs):
        print("get_form_class")
        if instance:  # it's an edit view
            return super().get_form_class(request, instance, **kwargs)
        else:  # it's a create view
            return UserWithProfileForm


# Now register the new UserProfileAdmin class with Wagtail
modeladmin_register(UserProfileAdmin)
