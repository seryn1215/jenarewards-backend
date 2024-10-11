# Generated by Django 4.2.3 on 2023-07-15 02:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='schedule',
        ),
        migrations.AddField(
            model_name='project',
            name='center_admins',
            field=models.ManyToManyField(limit_choices_to={'is_center_admin': True}, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=None),
        ),
    ]
