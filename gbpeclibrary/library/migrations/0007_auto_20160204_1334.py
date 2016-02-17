# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20160204_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='sem',
            field=models.IntegerField(default=1),
        ),
    ]
