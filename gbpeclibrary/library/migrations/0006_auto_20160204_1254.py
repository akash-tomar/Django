# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20160204_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='no_of_times_issued',
            new_name='total_no_of_times_issued',
        ),
    ]
