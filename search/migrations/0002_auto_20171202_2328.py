# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspaperarticle',
            name='publish_date',
        ),
        migrations.RemoveField(
            model_name='newspaperarticle',
            name='retrieval_date',
        ),
        migrations.AddField(
            model_name='newspaperarticle',
            name='keywords',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newspaperarticle',
            name='url',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]