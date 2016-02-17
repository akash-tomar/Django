# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20160203_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='no_of_times_issued',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='times_issued',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='no_of_books_issued',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text=b'Only Indian', max_length=128, unique=True, null=True, blank=True),
        ),
    ]
