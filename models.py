import datetime

from django.contrib.auth.models import User
from django.db import models
from uuidfield import UUIDField


class Project(models.Model):
    name = models.CharField(max_length=64, verbose_name="Project Name")
    description = models.CharField(max_length=2048,
                                   verbose_name="Project Description", blank=True)
    creation_date = models.DateTimeField('Date Created', auto_now=True,
                                         blank=True)
    user = models.ManyToManyField(User, blank=True,
                                  verbose_name="Project User")

    def __unicode__(self):
        return self.name


class Study(models.Model):
    name = models.CharField(max_length=64, verbose_name="Study Name", unique=True)
    project = models.ForeignKey(Project)
    description = models.CharField(max_length=256,
                                   verbose_name="Study Description",
                                   blank=True)
    creation_date = models.DateTimeField('Date Created', auto_now=True,
                                         blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Studies'


class Caller(models.Model):
    name = models.CharField(max_length=64, verbose_name="Caller Name")

    def __str__(self):
        return self.name


class Genome(models.Model):
    name = models.CharField(max_length=64, verbose_name="Genome")

    def __str__(self):
        return self.name


class Sample(models.Model):
    name = models.CharField(max_length=48, verbose_name='Sample Name', unique=True)
    description = models.CharField(max_length=256,
                                   verbose_name="Sample Description",
                                   blank=True)
    cellularity = models.CharField(max_length=8, verbose_name='% Cellularity',
                                   blank=True)
    study = models.ForeignKey(Study)
    creation_date = models.DateTimeField('Date Created', auto_now=True,
                                         blank=True)

    def __str__(self):
        return str(self.name)


class Bnid(models.Model):
    sample = models.ForeignKey(Sample)
    bnid = models.CharField(max_length=12, verbose_name='Bionimbus ID')
    description = models.CharField(max_length=256, verbose_name='Description',
                                   blank=True)
    library_type = models.CharField(max_length=32, verbose_name='Sequencing library type', blank=True)
    creation_date = models.DateTimeField('Date Created', auto_now=True,
                                         blank=True)

    def __str__(self):
        return '{} ({})'.format(str(self.sample), str(self.bnid))


# class Report(models.Model):
#     caller = models.ForeignKey(Caller)
#     study = models.ForeignKey(Study)
#     name = models.CharField(max_length=256, verbose_name='Report Name', default='report')
#     genome = models.ForeignKey(Genome, default=1, blank=True)
#     upload_date = models.DateTimeField('Date Uploaded', auto_now=True)
#     bnids = models.ManyToManyField(Bnid, verbose_name='Bionimbus ID', blank=True)
#     report_file = models.FileField('Report File', upload_to='', blank=True,
#                                    null=True)
#
#     def show_bnids(self):
#         return "_".join([a.bnid for a in self.bnids.all()])
#
#     def __str__(self):
#         return str(self.report_file)


# class Variant(models.Model):
#     report = models.ForeignKey(Report)
#     chrom = models.CharField(max_length=24, verbose_name='Chrom')
#     pos = models.IntegerField(verbose_name='Position', null=True)
#     ref = models.CharField(max_length=256, verbose_name='Reference Allele',
#                            blank=True, null=True)
#     alt = models.CharField(max_length=256, verbose_name='Alternate Allele',
#                            blank=True, null=True)
#     normal_ref_count = models.IntegerField(verbose_name='Normal Ref Count',
#                                            blank=True, null=True)
#     normal_alt_count = models.IntegerField(verbose_name='Normal Alt Count',
#                                            blank=True, null=True)
#     pct_normal_alt = models.FloatField(verbose_name='%_Normal_Alt',
#                                        blank=True, null=True)
#     tumor_ref_count = models.IntegerField(verbose_name='Tumor Ref Count',
#                                           blank=True, null=True)
#     tumor_alt_count = models.IntegerField(verbose_name='Tumor Alt Count',
#                                           blank=True, null=True)
#     pct_tumor_alt = models.FloatField(verbose_name='%_Tumor_Alt',
#                                       blank=True, null=True)
#     tn_pct_alt_ratio = models.FloatField(verbose_name='T/N % alt ratio',
#                                          blank=True, null=True)
#     gene_name = models.CharField(max_length=32, verbose_name='Gene Name',
#                                  blank=True, null=True)
#     extra_info = models.CharField(verbose_name='Extra Info', blank=True,
#                                   null=True, max_length=20000)
#
#     def __str__(self):
#         return "{}:{}{}>{}".format(self.chrom, self.pos, self.ref, self.alt)


class Contact(models.Model):
    full_name = models.CharField(max_length=256, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email')
    project = models.ForeignKey(Project, verbose_name='Project',
                                blank=True, null=True)

    def __unicode__(self):
        return '"{}" <{}>'.format(self.full_name, self.email)


class SharedData(models.Model):
    name = models.CharField(max_length=128, verbose_name='Shared Data Name')
    description = models.TextField(verbose_name='Shared Data Description')
    uuid = UUIDField(auto=True, hyphenate=True, blank=True,
                     null=True)  # defaults to v.4
    # report = models.ForeignKey(Report)
    field_lookup = models.TextField(verbose_name='Field Lookup JSON')
    creation_date = models.DateField(verbose_name='Creation Date',
                                     default=datetime.date.today)
    inactive_date = models.DateField(verbose_name='Inactive Date')
    shared_recipient = models.ManyToManyField(Contact,
                                              verbose_name='Shared Recipient')
    user = models.ForeignKey(User, verbose_name="Project User")

    def __unicode__(self):
        return str(self.uuid)

    class Meta:
        verbose_name_plural = 'Shared Data'


class HotListGene(models.Model):
    name = models.CharField(max_length=32, verbose_name='HotList Gene Name')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    viewable_studies = models.ManyToManyField(Study)


class Status(models.Model):
    bnid = models.ForeignKey(Bnid)
    study = models.ForeignKey(Study)
    sample = models.ForeignKey(Sample)
    submit_date = models.DateField(verbose_name='Submit for Sequence Date', blank=True, null=True)
    sequence_date = models.DateField(verbose_name='Sequence Date', blank=True, null=True)
    align_date = models.DateField(verbose_name='Align Date', blank=True, null=True)
    analysis_date = models.DateField(verbose_name='Date Analyzed', blank=True, null=True)
    status = models.CharField(max_length=256, verbose_name='Sample Status', default='Keys generated')

    def __str__(self):
        return '{}: {}'.format(str(self.bnid), str(self.status))

    class Meta:
        verbose_name_plural = 'Statuses'
