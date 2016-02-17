# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_auto_20160204_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='no_of_books_book_bank',
            field=models.IntegerField(default=0),
        ),
    ]
