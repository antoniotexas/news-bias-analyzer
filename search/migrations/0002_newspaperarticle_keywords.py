# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspaperarticle',
            name='keywords',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]