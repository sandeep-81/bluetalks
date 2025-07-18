# Generated by Django 5.1.4 on 2025-02-05 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_freindrequest_rece_alter_freindrequest_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freindrequest',
            name='rece',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rece', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='freindrequest',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
    ]
