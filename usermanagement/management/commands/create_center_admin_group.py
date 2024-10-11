from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from projects.models import Project


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="center_admins")
        # if created:
        project_content_type = ContentType.objects.get_for_model(Project)
        # get the 'change' permission for the Project model
        change_project_permission = Permission.objects.get(
            content_type=project_content_type, codename="change_project"
        )
        wagtail_admin_permission = Permission.objects.get(codename="access_admin")

        # assign the 'change' permission to the center_admins group
        group.permissions.add(change_project_permission)

        # Grant 'center_admins' the 'access Wagtail admin' permission
        group.permissions.add(wagtail_admin_permission)
        self.stdout.write(
            self.style.SUCCESS("Successfully created group Center Admins")
        )
        # else:
        #     self.stdout.write(self.style.SUCCESS("Group Center Admins already exists"))
