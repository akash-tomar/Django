# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20160204_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'Only Indian', max_length=128, null=True, blank=True),
        ),
    ]
