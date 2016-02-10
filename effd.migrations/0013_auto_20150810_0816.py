# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0012_auto_20150724_1121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='study',
            options={'verbose_name_plural': 'studies'},
        ),
        migrations.RenameField(
            model_name='variant',
            old_name='dbSnp_id',
            new_name='dbsnp_id',
        ),
        migrations.AlterField(
            model_name='report',
            name='bnids',
            field=models.ManyToManyField(to='viewer.Bnid', verbose_name=b'Bionimbus ID', blank=True),
            preserve_default=True,
        ),
    ]
