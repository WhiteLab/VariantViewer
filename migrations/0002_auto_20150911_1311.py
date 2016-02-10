# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=256, verbose_name=b'Full Name')),
                ('email', models.EmailField(max_length=75, verbose_name=b'Email')),
                ('project', models.ForeignKey(verbose_name=b'Project', blank=True, to='viewer.Project', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SharedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name=b'Shared Data Name')),
                ('uuid', uuidfield.fields.UUIDField(max_length=32, unique=True, null=True, editable=False, blank=True)),
                ('field_lookup', models.TextField(verbose_name=b'Field Lookup JSON')),
                ('creation_date', models.DateField(default=datetime.date.today, verbose_name=b'Creation Date')),
                ('inactive_date', models.DateField(verbose_name=b'Inactive Date')),
                ('shared_recipient', models.ManyToManyField(to='viewer.Contact', verbose_name=b'Shared Recipient')),
                ('user', models.ForeignKey(verbose_name=b'Project User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Shared Data',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'Project User', blank=True),
            preserve_default=True,
        ),
    ]
