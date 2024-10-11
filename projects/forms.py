from wagtail.admin.forms import WagtailAdminModelForm
from django import forms

from wagtail.admin.widgets import AdminTimeInput as TimeInput

from projects.models import Project


class ProjectAdminForm(WagtailAdminModelForm):
    def save(self, commit=True, *args, **kwargs):
        instance = super(ProjectAdminForm, self).save(commit=False, *args, **kwargs)

        print("New Save form", instance)
        print("User", kwargs.get("user", None))
        # Modify the instance here based on self.user
        # Example: instance.created_by = self.user

        if commit:
            instance.save()
        return instance
