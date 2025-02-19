# Generated by Django 4.2.3 on 2023-07-15 04:03

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CenterAdmin',
            fields=[
            ],
            options={
                'verbose_name': 'Center Admin',
                'verbose_name_plural': 'Center Admins',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('usermanagement.customuser',),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('usermanagement.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
