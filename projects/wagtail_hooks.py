from projects.forms import ProjectAdminForm
from projects.models import Project
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.helpers import PermissionHelper
from django.contrib.contenttypes.models import ContentType
from wagtail.models import Orderable, Page
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    FieldRowPanel,
    PanelGroup,
)
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django import forms

from usermanagement.models import CustomUser


class ProjectAdminPermissionHelper(PermissionHelper):
    def get_all_model_permissions(self):
        content_type = ContentType.objects.get_for_model(
            self.opts.model, for_concrete_model=False
        )
        return content_type.permission_set.all()

    # Ensure the user can add a project
    def user_can_create(self, user):
        return user.is_center_admin

    # Check if the user can edit a project
    def user_can_edit_obj(self, user, obj):
        print("pk", user.pk)
        print("center_admins", obj.center_admins.all())
        return user.is_superuser or (
            user.is_center_admin and obj.center_admins.filter(pk=user.pk).exists()
        )

    # Check if the user can delete a project
    def user_can_delete_obj(self, user, obj):
        return user.is_superuser or (
            user.is_center_admin and obj.center_admins.filter(pk=user.pk).exists()
        )


class ProjectAdmin(ModelAdmin):
    model = Project
    menu_label = "Projects"
    permission_helper_class = ProjectAdminPermissionHelper
    menu_icon = "folder-open-inverse"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "name",
        "start_date",
        "end_date",
        "coins",
        "max_participants",
        "view_qr_code",
        "view_activity_code",
    )
    search_fields = ("name", "start_date", "end_date")

    add_form = ProjectAdminForm

    def view_qr_code(self, obj):
        obj.generate_qr_code()
        url = reverse("qr_code", args=[obj.slug])

        return format_html(f'<a href="{url}" target="_blank">View QR Code</a>')

    def view_activity_code(self, obj):
        obj.generate_activity_code()
        url = reverse("activity_code", args=[obj.pk])

        return format_html(f'<a href="{url}" target="_blank">View Activity Code</a>')

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print("request.user.is_superuser", request.user.is_superuser)
        if request.user.is_center_admin:
            print("request.user.is_center_admin", request.user.is_center_admin)
            print("request.user.pk", request.user.username)
            custom_user = CustomUser.objects.get(pk=request.user.pk)
            print("custom_user", custom_user)
            # Limit projects to the ones assigned to the center admin
            return qs.filter(center_admins__in=[request.user])
        return qs

    def save_model(self, request, obj, form, change):
        print("save_model")
        if not change:
            print("not change")
            print("request.user.is_superuser", request.user.is_superuser)
            print("request.user.is_center_admin", request.user.is_center_admin)
            if not request.user.is_superuser and request.user.is_center_admin:
                custom_user = CustomUser.objects.get(pk=request.user.pk)
                obj.center_admins.add(custom_user)
        super().save_model(request, obj, form, change)

    panels = [
        FieldPanel("name"),
        FieldPanel("coins"),
        FieldPanel("max_participants"),
        FieldPanel("participants", heading="Participants"),
        FieldPanel("max_activity_per_day"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("center_admins"),
        FieldRowPanel(
            [
                FieldPanel(
                    "mon",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("mon_start_time", heading="start", classname="col2"),
                FieldPanel("mon_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Monday",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "tue",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("tue_start_time", heading="start", classname="col2"),
                FieldPanel("tue_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Tuesday",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "wed",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("wed_start_time", heading="start", classname="col2"),
                FieldPanel("wed_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Wednesday",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "thu",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("thu_start_time", heading="start", classname="col2"),
                FieldPanel("thu_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Thursday",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "fri",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("fri_start_time", heading="start", classname="col2"),
                FieldPanel("fri_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Friday",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "sat",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("sat_start_time", heading="start", classname="col2"),
                FieldPanel("sat_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Saturday",
        ),
        FieldRowPanel(
            [
                FieldPanel(
                    "sun",
                    widget=forms.CheckboxInput(),
                    heading="_",
                    classname="col1",
                ),
                FieldPanel("sun_start_time", heading="start", classname="col2"),
                FieldPanel("sun_end_time", heading="end", classname="col2"),
            ],
            classname="custom-field-row-panel",
            heading="Sunday",
        ),
    ]


modeladmin_register(ProjectAdmin)


class ProjectPage(Page):
    project = models.OneToOneField(Project, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=255, blank=False, null=False)
    center_admins = models.ManyToManyField(
        "usermanagement.CustomUser",
        limit_choices_to={"is_center_admin": True},
        related_name="project_pages",
    )

    content_panels = Page.content_panels + [
        # FieldPanel("project.name", classname="full"),
        # FieldPanel("project.center_admins", classname="full"),
        # FieldPanel("project.max_participants", classname="full"),
        # FieldPanel("project.start_date", classname="full"),
        # FieldPanel("project.end_date", classname="full"),
        # You can add more FieldPanel entries for other fields as needed.
        FieldPanel("name", classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["project"] = self.project
        return context
