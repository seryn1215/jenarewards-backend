from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, Manager
from django.contrib.contenttypes.models import ContentType
from django.forms import BooleanField, CheckboxInput, TextInput
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.contrib.auth.models import Group

from wagtail.admin import widgets
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    is_center_admin = models.BooleanField(default=False)
    uid = models.CharField(max_length=255, null=True, blank=True, unique=True)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.CharField(max_length=255, null=True, blank=True)
    coins = models.PositiveIntegerField(null=True, default=0)

    @property
    def calculated_coins(self):
        activities = self.activities.all()
        coins = self.coins or 0
        for activity in activities:
            coins += activity.credited_coins
        return coins

    # panels = [
    #     FieldPanel("user__username"),
    #     FieldPanel("user__email"),
    #     FieldPanel("image"),
    #     FieldPanel("coins"),
    # ]

    @classmethod
    def get_edit_handler(cls):
        panels = (
            [
                FieldPanel("user__username"),
                FieldPanel("user__email"),
                FieldPanel("user__password"),
            ],
        )
        edit_handler = MultiFieldPanel(panels, heading="User Profile")
        return edit_handler.bind_to_model(cls)

    def __str__(self):
        return f"{self.user.username}"


class CenterAdminPermissionHelper(PermissionHelper):
    def get_all_model_permissions(self):
        content_type = ContentType.objects.get_for_model(
            self.opts.model, for_concrete_model=False
        )
        return content_type.permission_set.all()


class CenterAdmin(CustomUser):
    panels = [
        FieldPanel("username"),
        FieldPanel("email"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("password"),
        FieldPanel("is_active"),
    ]

    class Meta:
        proxy = True
        verbose_name = "Center Admin"
        verbose_name_plural = "Center Admins"

    def save(self, *args, **kwargs):
        self.is_center_admin = True
        self.password = make_password(self.password)

        super().save(*args, **kwargs)
        self.groups.add(Group.objects.get(name="center_admins"))


class UserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_center_admin=False)


class User(CustomUser):
    is_center_admin = False

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_center_admin = False
        super().save(*args, **kwargs)
