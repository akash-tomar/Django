# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('roll_number', models.CharField(unique=True, max_length=30)),
                ('student_name', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=20)),
                ('sem', models.IntegerField(default=1)),
                ('pic', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('due_fine', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_name', models.CharField(max_length=200, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('is_issued', models.BooleanField(default=False)),
                ('dep_book', models.CharField(max_length=20)),
                ('book_name', models.CharField(max_length=200)),
                ('date_of_issue', models.DateField(default=b'1900-1-1')),
                ('return_date', models.DateField(default=b'1900-1-1')),
                ('book_added_on', models.DateField(default=b'1900-1-1')),
                ('placed_at_shelf', models.CharField(max_length=200, null=True, blank=True)),
                ('edition_of_book', models.IntegerField()),
                ('rare_book', models.BooleanField(default=False)),
                ('claim_one', models.CharField(max_length=30, null=True, blank=True)),
                ('claim_two', models.CharField(max_length=30, null=True, blank=True)),
                ('claim_three', models.CharField(max_length=30, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LastFiveIssues',
            fields=[
                ('lfi_id', models.AutoField(serialize=False, primary_key=True)),
                ('one_st', models.CharField(max_length=30, null=True, blank=True)),
                ('two_st', models.CharField(max_length=30, null=True, blank=True)),
                ('three_st', models.CharField(max_length=30, null=True, blank=True)),
                ('four_st', models.CharField(max_length=30, null=True, blank=True)),
                ('five_st', models.CharField(max_length=30, null=True, blank=True)),
                ('issue_one_date', models.DateField(null=True, blank=True)),
                ('issue_two_date', models.DateField(null=True, blank=True)),
                ('issue_three_date', models.DateField(null=True, blank=True)),
                ('issue_four_date', models.DateField(null=True, blank=True)),
                ('issue_five_date', models.DateField(null=True, blank=True)),
                ('return_one_date', models.DateField(null=True, blank=True)),
                ('return_two_date', models.DateField(null=True, blank=True)),
                ('return_three_date', models.DateField(null=True, blank=True)),
                ('return_four_date', models.DateField(null=True, blank=True)),
                ('return_five_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'last five issues',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('publisher_name', models.CharField(max_length=200, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('q_id', models.AutoField(serialize=False, primary_key=True)),
                ('book_name', models.CharField(max_length=200)),
                ('qty', models.IntegerField(default=1)),
                ('list_of_authors', models.ManyToManyField(to='library.Author')),
            ],
            options={
                'verbose_name_plural': 'Quantity',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ForeignKey(to='library.Quantity'),
        ),
        migrations.AddField(
            model_name='book',
            name='last_five_issues',
            field=models.OneToOneField(to='library.LastFiveIssues'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher_book',
            field=models.ForeignKey(to='library.Publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
