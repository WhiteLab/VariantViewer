# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_auto_20150911_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotListGene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'HotList Gene Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='name',
            field=models.CharField(default=b'report', max_length=256, verbose_name=b'Report Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shareddata',
            name='description',
            field=models.TextField(default=' ', verbose_name=b'Shared Data Description'),
            preserve_default=False,
        ),
    ]
