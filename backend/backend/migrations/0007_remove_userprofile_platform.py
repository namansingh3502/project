# Generated by Django 4.1.7 on 2023-04-27 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_userprofile_platform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='platform',
        ),
    ]