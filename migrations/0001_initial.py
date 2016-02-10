# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bnid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bnid', models.CharField(max_length=12, verbose_name=b'Bionimbus ID')),
                ('description', models.CharField(max_length=256, verbose_name=b'Description', blank=True)),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name=b'Date Created')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Caller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'Caller Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=256, verbose_name=b'Full Name')),
                ('email', models.EmailField(max_length=75, verbose_name=b'Email')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'Genome')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'Project Name')),
                ('description', models.CharField(max_length=2048, verbose_name=b'Project Description')),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name=b'Date Created')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'Project User', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'report', max_length=256, verbose_name=b'Report Name')),
                ('upload_date', models.DateTimeField(auto_now=True, verbose_name=b'Date Uploaded')),
                ('report_file', models.FileField(upload_to=b'', null=True, verbose_name=b'Report File', blank=True)),
                ('bnids', models.ManyToManyField(to='viewer.Bnid', verbose_name=b'Bionimbus ID', blank=True)),
                ('caller', models.ForeignKey(to='viewer.Caller')),
                ('genome', models.ForeignKey(default=1, blank=True, to='viewer.Genome')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=48, verbose_name=b'Sample Name')),
                ('description', models.CharField(max_length=256, verbose_name=b'Sample Description', blank=True)),
                ('cellularity', models.CharField(max_length=8, verbose_name=b'% Cellularity', blank=True)),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name=b'Date Created')),
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
                ('description', models.TextField(verbose_name=b'Shared Data Description')),
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
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'Study Name')),
                ('description', models.CharField(max_length=256, verbose_name=b'Study Description', blank=True)),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name=b'Date Created')),
                ('project', models.ForeignKey(to='viewer.Project')),
            ],
            options={
                'verbose_name_plural': 'Studies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chrom', models.CharField(max_length=24, verbose_name=b'Chrom')),
                ('pos', models.IntegerField(null=True, verbose_name=b'Position')),
                ('ref', models.CharField(max_length=256, null=True, verbose_name=b'Reference Allele', blank=True)),
                ('alt', models.CharField(max_length=256, null=True, verbose_name=b'Alternate Allele', blank=True)),
                ('normal_ref_count', models.IntegerField(null=True, verbose_name=b'Normal Ref Count', blank=True)),
                ('normal_alt_count', models.IntegerField(null=True, verbose_name=b'Normal Alt Count', blank=True)),
                ('pct_normal_alt', models.FloatField(null=True, verbose_name=b'%_Normal_Alt', blank=True)),
                ('tumor_ref_count', models.IntegerField(null=True, verbose_name=b'Tumor Ref Count', blank=True)),
                ('tumor_alt_count', models.IntegerField(null=True, verbose_name=b'Tumor Alt Count', blank=True)),
                ('pct_tumor_alt', models.FloatField(null=True, verbose_name=b'%_Tumor_Alt', blank=True)),
                ('tn_pct_alt_ratio', models.FloatField(null=True, verbose_name=b'T/N % alt ratio', blank=True)),
                ('gene_name', models.CharField(max_length=32, null=True, verbose_name=b'Gene Name', blank=True)),
                ('extra_info', models.CharField(max_length=20000, null=True, verbose_name=b'Extra Info', blank=True)),
                ('report', models.ForeignKey(to='viewer.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sample',
            name='study',
            field=models.ForeignKey(to='viewer.Study'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='study',
            field=models.ForeignKey(to='viewer.Study'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='project',
            field=models.ForeignKey(verbose_name=b'Project', blank=True, to='viewer.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bnid',
            name='sample',
            field=models.ForeignKey(to='viewer.Sample'),
            preserve_default=True,
        ),
    ]
