# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(default=b'cse', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_name',
            field=models.CharField(default=b'student', max_length=200),
        ),
    ]
