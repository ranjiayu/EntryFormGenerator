# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_form_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='maxcount',
            field=models.IntegerField(null=True),
        ),
    ]
