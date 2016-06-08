# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='aums_id',
            field=models.CharField(max_length=32, serialize=False, verbose_name='Aums ID', primary_key=True),
        ),
    ]
