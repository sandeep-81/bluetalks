# Generated by Django 5.1.4 on 2025-02-02 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='fullname',
            new_name='username',
        ),
    ]
