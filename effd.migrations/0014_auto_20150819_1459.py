# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0013_auto_20150810_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='amino_acid_change',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='amino_acid_length',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='coding',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='codon_change',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='context',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='dbsnp_id',
        ),
        migrations.RemoveField(
            model_name='variant',
            name='effect',
        ),
        migrations.AddField(
            model_name='variant',
            name='extra_info',
            field=models.CharField(max_length=20000, null=True, verbose_name=b'Extra Info', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='variant',
            name='pct_normal_alt',
            field=models.FloatField(null=True, verbose_name=b'%_Normal_Alt', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='variant',
            name='pct_tumor_alt',
            field=models.FloatField(null=True, verbose_name=b'%_Tormal_Alt', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='variant',
            name='tn_pct_alt_ratio',
            field=models.FloatField(null=True, verbose_name=b'T/N % alt ratio', blank=True),
            preserve_default=True,
        ),
    ]
