# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0011_auto_20150723_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='bnids',
            field=models.ManyToManyField(to='viewer.Bnid', verbose_name=b'Bionimbus ID'),
            preserve_default=True,
        ),
    ]
