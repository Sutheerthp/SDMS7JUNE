# Generated by Django 5.0.1 on 2024-06-08 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SDMSapp', '0003_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SDMSapp.item'),
        ),
    ]
