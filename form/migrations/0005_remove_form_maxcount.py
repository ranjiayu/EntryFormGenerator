# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 04:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_form_maxcount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form',
            name='maxcount',
        ),
    ]
