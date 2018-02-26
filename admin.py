from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from models import *


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('name', 'description', 'creation_date')
    filter_horizontal = ('user', )


class BnidAdmin(admin.ModelAdmin):
    model = Bnid
    list_display = ('__str__', 'description', 'creation_date')


class SampleAdmin(admin.ModelAdmin):
    model = Sample
    list_display =('id', 'name', 'creation_date')


class CallerAdmin(admin.ModelAdmin):
    display = ['name']


# class ReportAdmin(admin.ModelAdmin):
#     model = Report
#     list_display = ('study', 'show_bnids', 'caller', 'report_file', 'upload_date')


class StudyAdmin(admin.ModelAdmin):
    model = Study
    list_display = ('name', 'description')


class StatusAdmin(admin.ModelAdmin):
    model = Status
    list_display = ('study', 'bnid', 'sample', 'status')


class GenomeAdmin(admin.ModelAdmin):
    model = Genome
    list_display = ('id', 'name')


# class VariantAdmin(admin.ModelAdmin):
#     model = Variant
#     list_display = ('__str__', 'report', 'gene_name', 'chrom', 'pos', 'ref', 'alt',
#                     'normal_ref_count', 'normal_alt_count', 'tumor_ref_count',
#                     'tumor_alt_count')


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('full_name', 'email', 'project')


class SharedDataAdmin(admin.ModelAdmin):
    model = SharedData
    list_display = ('uuid', 'field_lookup', 'user', 'creation_date', 'inactive_date')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Bnid, BnidAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Caller, CallerAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Genome, GenomeAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(SharedData, SharedDataAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
