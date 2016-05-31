import simplejson
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from forms import (ProjectForm, ReportForm, StudyForm,
                   UserForm, SharedDataForm, ContactForm)
from models import *
from util import report_parser, render_charts


def index(request):
    return render(request, 'viewer/index.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            firstname = user_form['first_name'].value()
            lastname = user_form['last_name'].value()
            admin_url = '<a href="http://igsbimg.uchicago.edu/viewer/admin/auth/user/{}/">{}</a>'.format(
                user.id,
                request.POST.get('user_type')
            )
            subject = 'Report Viewer Registration: {}, {}'.format(
                lastname, firstname)
            message = 'User {} {} <{}> has registered and needs to be vetted.'.format(
                firstname, lastname, user.email)
            message += ' User is requesting {} status.'.format(
                admin_url
            )
            send_mail(subject, message, 'miguelb@uchicago.edu',
                      ['miguelb@uchicago.edu'], fail_silently=False)
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    context = {
        'user_form': user_form,
        'registered': registered,
        'viewer_admin_email': settings.VIEWER_ADMIN_EMAIL
    }
    context.update(csrf(request))
    return render_to_response('viewer/user/register.html', context,
                              context_instance=RequestContext(request))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('viewer_index'))
            else:
                # user is inactive
                return HttpResponse("Sorry, your account is disabled.")
        else:
            # Bad login details
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details provided.")
    else:
        context = {}
        context.update(csrf(request))
        return render(request, 'viewer/user/login.html', context)


def change_password(request):
    if request.method == 'POST':
        pass

    return HttpResponse('change password')


def restricted(request):
    return HttpResponse('You are not authorized to access this content.')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('viewer_index'))


'''
Project model
'''


@permission_required('viewer.add_project', login_url=reverse_lazy('viewer_restricted'))
def manage_project(request):
    context = {'projects': Project.objects.all()}
    context.update(csrf(request))
    return render_to_response('viewer/project/manage_project.html', context,
                              context_instance=RequestContext(request))


@permission_required('viewer.add_project', login_url=reverse_lazy('viewer_restricted'))
def new_project(request):
    if request.method == 'POST':
        pform = ProjectForm(request.POST, instance=Project())
        if pform.is_valid():
            pform.save()
        return HttpResponseRedirect(reverse('manage_project'))
    else:
        pform = ProjectForm(instance=Project())
        context = {'project_form': pform}
        context.update(csrf(request))
        return render_to_response('viewer/project/new_project.html', context,
                                  context_instance=RequestContext(request))


@permission_required('viewer.change_project', login_url=reverse_lazy('viewer_restricted'))
def edit_project(request, project_id):
    if request.method == 'POST':
        p = Project.objects.get(pk=project_id)
        updated_form = ProjectForm(request.POST, instance=p)
        if updated_form.is_valid():
            updated_form.save()
            return HttpResponseRedirect(reverse('manage_project'))
    else:
        proj_obj = Project.objects.get(pk=project_id)
        pform = ProjectForm(instance=proj_obj)
        context = {'project_form': pform, 'name': proj_obj.name,
                   'pk': proj_obj.pk}
        context.update(csrf(request))
        return render_to_response('viewer/project/edit_project.html',
                                  context,
                                  context_instance=RequestContext(request))


'''
Study model
'''


@permission_required('viewer.add_study', login_url=reverse_lazy('viewer_restricted'))
def manage_study(request, set_viewing_project_pk=None):
    project_pk = filter_on_project(request.user, request.session, set_viewing_project_pk)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    project = Project.objects.get(pk=project_pk)
    context = {
        'studies': project.study_set.all(),
        'project_name': project.name
    }
    context.update(csrf(request))
    return render_to_response('viewer/study/manage_study.html', context,
                              context_instance=RequestContext(request))


@permission_required('viewer.add_study', login_url=reverse_lazy('viewer_restricted'))
def new_study(request):
    if request.method == 'POST':
        sform = StudyForm(request.POST, instance=Study())
        if sform.is_valid():
            sform.save()
        return HttpResponseRedirect(reverse('manage_study'))
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        sform = StudyForm(instance=Study(), initial={'project': project_pk})
        context = {
            'study_form': sform,
            'project_name': Project.objects.get(pk=project_pk).name
        }
        context.update(csrf(request))
        return render_to_response('viewer/study/new_study.html', context,
                                  context_instance=RequestContext(request))


@permission_required('viewer.change_study', login_url=reverse_lazy('viewer_restricted'))
def edit_study(request, study_id):
    if request.method == 'POST':
        s = Study.objects.get(pk=study_id)
        updated_form = StudyForm(request.POST, instance=s)
        if updated_form.is_valid():
            updated_form.save()
            return HttpResponseRedirect(reverse('manage_study'))
    else:
        study_obj = Study.objects.get(pk=study_id)
        sform = StudyForm(instance=study_obj)
        context = {'study_form': sform, 'name': study_obj.name, 'pk': study_obj.pk}
        context.update(csrf(request))
        return render_to_response('viewer/study/edit_study.html', context,
                                  context_instance=RequestContext(request))


@permission_required('viewer.delete_study', login_url=reverse_lazy('viewer_restricted'))
def delete_study(request, study_id):
    if request.method == 'POST':
        Study.objects.get(pk=study_id).delete()
        return HttpResponseRedirect(reverse('manage_study'))
    else:
        study_obj = Study.objects.get(pk=study_id)
        context = {'name': study_obj.name, 'pk': study_obj.pk}
        context.update(csrf(request))
        return render_to_response('viewer/study/delete_study.html', context,
                                  context_instance=RequestContext(request))


'''
Merged Samples/BIDs into Metadata
'''


@login_required
def manage_metadata(request, set_viewing_project_pk=None):
    project_pk = filter_on_project(request.user, request.session, set_viewing_project_pk)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    project = Project.objects.get(pk=project_pk)
    viewable_studies = request.user.userprofile.viewable_studies.all()
    context = {
        'project_name': project.name,
        'samples': Sample.objects.filter(study__project__pk=project_pk).filter(study__in=viewable_studies),
    }
    return render(request, 'viewer/metadata/manage_metadata.html', context)


@permission_required('viewer.add_sample', login_url=reverse_lazy('viewer_restricted'))
def new_metadata(request):
    if request.method == 'POST':
        sheet_data = simplejson.loads(request.POST.get('sheet'))
        for row in sheet_data:
            (study_name, sample_name,
             bid, description, cellularity) = row
            if not Study.objects.filter(name=study_name).exists():
                # Notify user
                continue
            if not Sample.objects.filter(name=sample_name).exists():
                new_sample = Sample()
                new_sample.name = sample_name
                new_sample.description = description
                new_sample.cellularity = cellularity
                new_sample.study = Study.objects.get(name=study_name)
                new_sample.save()
            if not Bnid.objects.filter(bnid=bid).exists():
                new_bnid = Bnid()
                new_bnid.bnid = bid
                new_bnid.sample = Sample.objects.get(name=sample_name)
                new_bnid.save()
        return HttpResponseRedirect(reverse('manage_metadata'))
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        project = Project.objects.get(pk=project_pk)
        context = {
            'project_name': project.name
        }
        return render_to_response('viewer/metadata/new_metadata.html', context,
                                  context_instance=RequestContext(request))


@permission_required('viewer.change_sample', login_url=reverse_lazy('viewer_restricted'))
def edit_metadata(request, sample_id):
    if request.method == 'POST':
        sample = Sample.objects.get(pk=sample_id)

        new_bids = [new_bid.strip() for new_bid in request.POST.get('metadata_bids').split(',')]
        new_description = request.POST.get('metadata_description')
        new_cellularity = request.POST.get('metadata_cellularity')

        sample.description = new_description
        sample.cellularity = new_cellularity
        sample.save()


        old_bids = [bid for bid in sample.bnid_set.all()]
        for old_bid in old_bids:
            old_bid.delete()

        for new_bid in new_bids:
            new_bid_object = Bnid()
            new_bid_object.bnid = new_bid
            new_bid_object.sample = sample
            new_bid_object.save()


        print new_bids
        print new_description
        print new_cellularity



        # s = Study.objects.get(pk=study_id)
        # updated_form = StudyForm(request.POST, instance=s)
        # if updated_form.is_valid():
        #     updated_form.save()
        return HttpResponseRedirect(reverse('manage_metadata'))
    else:
        sample = Sample.objects.get(pk=sample_id)
        bids = sample.bnid_set.all()


        # study_obj = Study.objects.get(pk=study_id)
        # sform = StudyForm(instance=study_obj)
        # context = {'study_form': sform, 'name': study_obj.name, 'pk': study_obj.pk}
        # context.update(csrf(request))
        print sample.description
        metadata_fields = [
            {
                'id': 'metadata_bids',
                'label': 'Sample BIDs (comma separate for multiple):',
                'value': ','.join([bid.bnid for bid in bids])
            },
            {
                'id': 'metadata_description',
                'label': 'Sample Description:',
                'type': 'textarea',
                'value': sample.description
            },
            {
                'id': 'metadata_cellularity',
                'label': 'Sample Percent Cellularity:',
                'value': sample.cellularity
            }
        ]

        context = {
            'metadata_fields': metadata_fields,
            'pk': sample_id,
            'name': sample.name
        }
        context.update(csrf(request))
        return render(request, 'viewer/metadata/edit_metadata.html', context)

@permission_required('viewer.delete_sample', login_url=reverse_lazy('viewer_restricted'))
def delete_sample(request, sample_id):
    if request.method == 'POST':
        Sample.objects.get(pk=sample_id).delete()
        return HttpResponseRedirect(reverse('manage_metadata'))
    else:
        sample_obj = Sample.objects.get(pk=sample_id)
        context = {'name': sample_obj.name, 'pk': sample_obj.pk}
        context.update(csrf(request))
        return render(request, 'viewer/metadata/delete_sample.html', context)


'''
Status Model
'''

@login_required
def manage_status(request, set_viewing_project_pk=None):
    project_pk = filter_on_project(request.user, request.session, set_viewing_project_pk)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    project = Project.objects.get(pk=project_pk)
    viewable_studies = request.user.userprofile.viewable_studies.all()
    context = {
        'project_name': project.name,
        'statuses': Status.objects.filter(study__project__pk=project_pk).filter(study__in=viewable_studies),
    }
    return render(request, 'viewer/status/manage_status.html', context)

@permission_required('viewer.update_status', login_url=reverse_lazy('viewer_restricted'))
def update_status(request):
    from datetime import datetime
    update_req = simplejson.loads(request.readlines()[0])
    bid = update_req['bnid']
    bid_obj = Bnid.objects.get(bnid=bid)
    sample_obj = Sample.objects.get(pk=bid_obj.sample_id)
    # method returns flag as to whether or not it had to create an object
    try:
        (cur, cflag) = Status.objects.get_or_create(bnid=bid_obj, sample=sample_obj, study=sample_obj.study)

        for k in update_req:
            if k != 'bnid':
                value = update_req[k]
                if k[-4:] == 'date':
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                setattr(cur, k, value)
    except:
        error = 'No metadata for bid ' + bid
        return HttpResponse(error)
    try:
        print 'Saving new object'
        cur.save()
        json_response = cur.__dict__
        pretty = simplejson.dumps(json_response, sort_keys=True, indent=4)
        return HttpResponse(pretty)
    except Exception as e:
        error = {'Message': e.message}
        return HttpResponse(error)


@permission_required('viewer.check_status', login_url=reverse_lazy('viewer_restricted'))
def check_status(request):
    check_req = simplejson.loads(request.readlines()[0])
    bid = check_req['bnid']
    bid_obj = Bnid.objects.get(bnid=bid)
    cur = Status.objects.get(bnid=bid_obj.pk)
    return simplejson.dumps(cur.__dict__, content_type="application/json")


'''
Report model
'''


@login_required
def manage_report(request, set_viewing_project_pk=None):
    project_pk = filter_on_project(request.user, request.session, set_viewing_project_pk)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    viewable_studies = request.user.userprofile.viewable_studies.all()
    context = {
        'reports': Report.objects.filter(study__project__pk=project_pk).filter(study__in=viewable_studies),
        'project_name': Project.objects.get(pk=project_pk).name,
        'variant_fields': Variant._meta.get_all_field_names()
    }
    context.update(csrf(request))
    return render(request, 'viewer/report/manage_report.html', context)


@permission_required('viewer.add_report', login_url=reverse_lazy('viewer_restricted'))
def upload_report(request):
    if request.method == 'POST':
        print "POST from upload_report"
        if request.FILES:
            rform = ReportForm(request.POST, request.FILES)
        else:
            rform = ReportForm(request.POST)
        if rform.is_valid():
            report = rform.save()
            report_parser.load_into_db(report)
            return HttpResponseRedirect(reverse('manage_report'))
        else:
            print "rform (ReportForm) is Invalid"
            print str(rform)
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        project = Project.objects.get(pk=project_pk)
        rform = ReportForm(instance=Report(), initial={})
        rform.fields['study'].queryset = project.study_set.all()
        context = {'report_form': rform}
        context.update(csrf(request))
        return render_to_response('viewer/report/upload_report.html', context,
                                  context_instance=RequestContext(request))


@permission_required('viewer.change_report', login_url=reverse_lazy('viewer_restricted'))
def edit_report(request, report_id):
    if request.method == 'POST':
        r = Report.objects.get(pk=report_id)
        if request.FILES:
            updated_form = ReportForm(request.POST, request.FILES, instance=r)
            r.variant_set.all().delete()
        else:
            updated_form = ReportForm(request.POST, instance=r)
        if updated_form.is_valid():
            updated_form.save()
            report_parser.load_into_db(r)
            return HttpResponseRedirect(reverse('manage_report'))
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        project = Project.objects.get(pk=project_pk)
        report_obj = Report.objects.get(pk=report_id)
        rform = ReportForm(instance=report_obj)
        rform.fields['study'].queryset = project.study_set.all()
        context = {'report_form': rform,
                   'report': report_obj.report_file,
                   'pk': report_id,}
        context.update(csrf(request))
        return render_to_response('viewer/report/edit_report.html', context,
                                  context_instance=RequestContext(request))


@login_required
def view_report(request, file_id):
    # build context from file
    print 'file_id: %s' % file_id
    report_obj = Report.objects.get(pk=file_id)

    # Ajaxy version to grab variants from db
    variants = report_obj.variant_set.all()
    # print report_data
    report_html = str(report_parser.json_from_ajax(variants))

    # load from file version
    # report_data = report_parser.json_from_report(
    #     os.path.join(report_parser.get_media_path(),
    #                  report_obj.report_file.name))
    # report_html = str(report_data.html)

    # add table class and id
    replace_string = "<table class=\"table table-hover\" id=\"report-table\">"
    report_html = report_html.replace("<table>", replace_string)

    context = {'report_html': report_html,
               'viewing_report': True,
               'filename': report_obj.report_file.name.split('/')[1],
               'study': report_obj.bnids.first().sample.study,
               'report_obj': report_obj}
    return render(request, 'viewer/report/view_report.html', context)


# get info to upload reports
@csrf_exempt
def report_info_get(request):
    try:
        info_req = simplejson.loads(request.readlines()[0])
        (bid, caller_name, genome_name) = (
            info_req['bid'], info_req['caller'], info_req['genome'])
        report_info = Bnid.objects.get(bnid=bid)
        caller_info = Caller.objects.get(name=caller_name)
        genome_info = Genome.objects.get(name=genome_name)

        bid_pk = report_info.pk
        sample = report_info.sample.name
        study = report_info.sample.study.pk
        description = report_info.sample.description
        caller_pk = caller_info.pk
        genome_pk = genome_info.pk

        json_response = {'bid_pk': bid_pk,
                         'sample': sample,
                         'study': study,
                         'description': description,
                         'caller_pk': caller_pk,
                         'genome_pk': genome_pk}

        pretty = simplejson.dumps(json_response, sort_keys=True, indent=4)
        return HttpResponse(pretty)
    except Exception as e:
        error = {'Message': e.message}
        return HttpResponse(error)


@permission_required('viewer.delete_report', login_url=reverse_lazy('viewer_restricted'))
def delete_report(request, report_id):
    if request.method == 'POST':
        Report.objects.get(pk=report_id).delete()
        return HttpResponseRedirect(reverse('manage_report'))
    else:
        report_obj = Report.objects.get(pk=report_id)
        context = {'name': report_obj.report_file.name.strip('./'), 'pk': report_obj.pk}
        return render(request, 'viewer/report/delete_report.html', context)


'''
Contact model
'''


# TODO Need to decide whether this model matters or not


@login_required
def manage_contact(request, set_viewing_project_pk=None):
    project_pk = filter_on_project(request.user, request.session, set_viewing_project_pk)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    project = Project.objects.get(pk=project_pk)
    context = {
        'contacts': project.contact_set.all(),
        'project_name': project.name
    }
    context.update(csrf(request))
    return render(request, 'viewer/contact/manage_contact.html', context)


@login_required
def new_contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, instance=Contact())
        if contact_form.is_valid():
            contact_form.save()
        return HttpResponseRedirect(reverse('manage_contact'))
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        contact_form = ContactForm(instance=Contact(), initial={'project': project_pk})
        context = {
            'contact_form': contact_form,
            'project_name': Project.objects.get(pk=project_pk).name
        }
        context.update(csrf(request))
        return render_to_response('viewer/contact/new_contact.html', context,
                                  context_instance=RequestContext(request))


@login_required
def new_contact_from_share(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, instance=Contact())
        if contact_form.is_valid():
            contact_form.save()
        return HttpResponseRedirect(reverse('manage_contact'))
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        contact_form = ContactForm(instance=Contact(), initial={'project': project_pk})
        context = {
            'contact_form': contact_form,
            'project_name': Project.objects.get(pk=project_pk).name
        }
        context.update(csrf(request))
        return render_to_response('viewer/contact/new_contact_from_share.html', context,
                                  context_instance=RequestContext(request))


@login_required
def edit_contact(request, contact_id):
    if request.method == 'POST':
        contact = Contact.objects.get(pk=contact_id)
        updated_form = ContactForm(request.POST, instance=contact)
        if updated_form.is_valid():
            updated_form.save()
            return HttpResponseRedirect(reverse('manage_contact'))
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        contact = Contact.objects.get(pk=contact_id)
        contact_form = ContactForm(instance=contact)
        context = {
            'contact_form': contact_form,
            'name': contact.full_name,
            'pk': contact.pk,
            'project_name': Project.objects.get(pk=project_pk).name
        }
        context.update(csrf(request))
        return render_to_response('viewer/contact/edit_contact.html', context,
                                  context_instance=RequestContext(request))


@login_required
def delete_contact(request, contact_id):
    if request.method == 'POST':
        Contact.objects.get(pk=contact_id).delete()
        return HttpResponseRedirect(reverse('manage_contact'))
    else:
        contact = Contact.objects.get(pk=contact_id)
        context = {'name': contact.full_name, 'pk': contact.pk}
        context.update(csrf(request))
        return render(request, 'viewer/contact/delete_contact.html', context)


@csrf_exempt
def get_contacts_json(request, project_id):
    contacts = Project.objects.get(pk=project_id).contact_set.all()
    contacts_json = {}
    for contact in contacts:
        contacts_json[contact.pk] = str(contact)
    return HttpResponse(simplejson.dumps(contacts_json))


'''
Search functions
'''


@login_required
def search_reports(request, set_viewing_project_pk=None):
    project_pk = filter_on_project(request.user, request.session, set_viewing_project_pk)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    variant_fields = Variant._meta.get_all_field_names()
    num_reports = len(
        list(set(Variant.objects.values_list('report', flat=True).filter(report__study__project__pk=project_pk))))
    context = {
        'variant_fields': variant_fields,
        'num_reports': num_reports,
        'project_name': Project.objects.get(pk=project_pk).name
    }
    return render(request, 'viewer/search/search_reports.html', context)


@login_required
@csrf_exempt
def ajax_search_reports(request, search_col, search_term, search_type):
    project_pk = request.session.get('viewing_project', None)
    if project_pk is None:
        return HttpResponseRedirect(reverse('no_project'))
    db_lookup = '__'.join([search_col, search_type])
    variants = Variant.objects.all()
    if request.POST.get('report_ids'):
        report_ids = simplejson.loads(request.POST.get('report_ids'))
        variants = variants.filter(report_id__in=report_ids)
    variants = (variants.filter(report__study__project__pk=project_pk)
                .filter(**{db_lookup: search_term}))
    return HttpResponse(report_parser.json_from_ajax(variants))


'''
Shared Reports
'''


def view_shared_data(request, shared_data_uuid):
    shared_report = SharedData.objects.filter(uuid__iexact=shared_data_uuid)
    if len(shared_report) == 0:
        return HttpResponse(reverse('shared_data_dne'))
    shared_report = shared_report[0]
    if shared_report.inactive_date < datetime.date.today():
        return HttpResponse(reverse('shared_data_expired'))

    field_lookup = simplejson.loads(shared_report.field_lookup)
    variants = Variant.objects.filter(**field_lookup)

    report_html = str(report_parser.json_from_ajax(variants))

    replace_string = "<table class=\"table table-hover\" id=\"report-table\">"
    report_html = report_html.replace("<table>", replace_string)

    context = {'report_html': report_html,
               'viewing_report': False,
               'shared_data_name': shared_report.name}
    return render(request, 'viewer/report/view_report.html', context)


def view_share_data_expired(request):
    return render(request, 'viewer/error/share_data_expired.html')


def view_share_data_dne(request):
    return render(request, 'viewer/error/share_data_dne.html')


# @user_passes_test(in_proj_user_group)
# def share_report(request, report_id=None):
#     if request.method == 'POST':
#         shared_data_form = SharedDataForm(request.POST, instance=SharedData())
#         if shared_data_form.is_valid():
#             shared_data = shared_data_form.save(commit=False)
#             shared_data.user = request.user
#             shared_data.creation_date = date.today()
#             shared_data.save()
#             shared_data_form.save_m2m()
#             # format the email better here TODO
#             subject = 'Shared Variant Report: {}'.format(
#                 shared_data_form['name'].value())
#             absolute_uri = request.build_absolute_uri('/')
#             uuid = str(shared_data.uuid).replace('-', '')
#             share_url = absolute_uri + 'viewer/shared/view/' + uuid + '/'
#             recipients = [str(contact) for contact in shared_data.shared_recipient.all()]
#
#             message = 'A variant report has been shared with you. Go to the following link to view: '
#             message += share_url
#
#             print subject
#             print message
#
#             send_mail(subject, message, 'no-reply@uchicago.edu',
#                       recipients, fail_silently=False)
#
#         return HttpResponseRedirect('/viewer/report/')
#             # I don't know that we should necessarily redirect
#             # Maybe just close the modal box, return to page?
#             # but then how do we assure success? Or report failure? TODO
#     else:
#         project_pk = request.session.get('viewing_project', None)
#         if project_pk is None:
#             return HttpResponseRedirect(reverse('no_project)
#         report = Report.objects.get(pk=report_id)
#         shared_data_form = SharedDataForm(instance=SharedData(), initial={
#             'field_lookup': simplejson.dumps({'report_id': report_id})
#         })
#         shared_data_form.fields['shared_recipient'].queryset = Project.objects.get(pk=project_pk).contact_set.all()
#         context = {
#             'report_name': report.report_file.name[2:],
#             'shared_data_form': shared_data_form
#         }
#         return render(request, 'viewer/share/share_report.html', context)


def share_search(request):
    if request.method == 'POST':
        shared_data_form = SharedDataForm(request.POST, instance=SharedData())
    else:
        shared_data_form = SharedDataForm(instance=SharedData(), initial={
            'field_lookup': ''
        })


def new_shared_data(request):
    if request.method == 'POST':
        shared_data_form = SharedDataForm(request.POST, instance=SharedData())
        if shared_data_form.is_valid():
            shared_data_form.save()
        return HttpResponseRedirect


'''
Errors
'''


@login_required
def no_project(request):
    return render(request, 'viewer/error/no_project.html')


'''
Util functions
'''


@login_required
def get_samples(request, study_id=None, **kwargs):
    sample_dict = {}
    if study_id:
        study = Study.objects.get(pk=study_id)
        samples = Sample.objects.filter(study=study)
        for sample in samples:
            sample_dict[sample.id] = sample.name
    return HttpResponse(simplejson.dumps(sample_dict),
                        content_type="application/json")


@login_required
def get_bnids_by_study(request, study_id=None):
    print "study_id: {}".format(study_id)
    bnid_dict = dict()
    if study_id:
        study = Study.objects.get(pk=study_id)
        samples = Sample.objects.filter(study=study)
        for sample in samples:
            bnids = Bnid.objects.filter(sample=sample)
            for bnid in bnids:
                bnid_dict[bnid.id] = "{}".format(bnid)
    return HttpResponse(simplejson.dumps(bnid_dict),
                        content_type="application/json")


@login_required
def load_variants(request, report_id=None):
    print "Load Variants for Report ID: {}".format(report_id)
    report_obj = Report.objects.get(pk=report_id)
    report_parser.load_into_db(report_obj)
    return HttpResponseRedirect(reverse('manage_report'))


@login_required
def get_all_projects(request):
    project_dict = {}
    for p in Project.objects.all():
        project_dict[p.pk] = p.name
    return HttpResponse(simplejson.dump(project_dict),
                        content_type="application/json")


def filter_on_project(user, session, set_viewing_project_pk):
    if set_viewing_project_pk is not None:
        if user.project_set.filter(pk=set_viewing_project_pk).exists():
            session['viewing_project'] = set_viewing_project_pk
            return set_viewing_project_pk
    return session.get('viewing_project', None)


def populate_sidebar(request):
    current_user = request.user
    current_project_pk = request.session.get('viewing_project', None)
    if current_user.is_authenticated():
        nav_data = []
        for project in current_user.project_set.all():
            num_studies = project.study_set.all().count()
            num_samples = 0
            num_bnids = 0
            num_reports = 0
            for study in project.study_set.all():
                num_samples += study.sample_set.all().count()
                num_reports += study.report_set.all().count()
                # for sample in study.sample_set.all():
                #     num_bnids += sample.bnid_set.all().count()

            project_data = {
                'name': project.name,
                'pk': project.pk,
                'studies': num_studies,
                'samples': num_samples,
                # 'bnids': num_bnids,
                'reports': num_reports,
                'current': True if current_project_pk == str(project.pk) else False
            }
            nav_data.append(project_data)
        # print nav_data
        if len(nav_data) == 0:
            return HttpResponse('<li><a href="#">No Projects Available</a></li>')
        return render(request, 'viewer/sidebar/project_dropdowns.html', {'projects': nav_data})
    return HttpResponse('')


def info(request, report_id):
    report_pk = Report.objects.get(pk=report_id).pk
    return render(request, 'viewer/info/info.html', {'report_pk': report_pk})


def info_many(request):
    report_ids = request.GET.getlist('reportIds[]')
    return render(request, 'viewer/info/info.html', {'report_ids': simplejson.dumps(report_ids)})


'''
Cards functions
'''


def get_cards(request):
    context = {}
    card_names = request.GET.getlist('cards[]')
    report_ids = request.GET.getlist('report_ids[]')
    reports = Report.objects.filter(pk__in=report_ids)
    context.update({
        'reports': reports,
        'report_ids_json': simplejson.dumps(report_ids),
        'reports_list_string': ', '.join([report.name for report in reports]),
        'cards': card_names
    })
    if 'geneList' in card_names:
        context.update(render_gene_list(reports))
    if 'geneProfile' in card_names:
        context.update(render_gene_profile(reports, request.GET.get('gene_name')))
    return render(request, 'viewer/cards/cards.html', context)


def render_gene_profile(reports, gene_name):
    mutation_dict = {
        'A>C': 0,
        'A>G': 0,
        'A>T': 0,
        'C>A': 0,
        'C>G': 0,
        'C>T': 0,
        'G>A': 0,
        'G>C': 0,
        'G>T': 0,
        'T>A': 0,
        'T>C': 0,
        'T>G': 0
    }
    gene_count = 0

    for report in reports:
        gene = report.variant_set.filter(gene_name__exact=gene_name)
        gene_count += gene.count()
        for g in gene:
            mutation_dict[g.ref + '>' + g.alt] += 1

    print mutation_dict

    return {
        'gene': {
            'name': gene_name,
            'count': gene_count,
            'mutations': mutation_dict

        }
    }


def render_gene_list(reports):
    gene_list = []
    for report in reports:
        for variant in report.variant_set.all():
            if variant.gene_name not in gene_list:
                gene_list.append(variant.gene_name)
    gene_list.pop(gene_list.index(''))
    return {
        'gene_list': sorted(gene_list)
    }


def get_series_data(request):
    chart_name = request.GET.get('chartName')
    kwargs = simplejson.loads(request.GET.get('chartKwargs'))
    highchart = getattr(render_charts, chart_name)(**kwargs)
    context = {
        'chart_name': chart_name,
        'highchart': highchart
    }
    return HttpResponse(simplejson.dumps(context))


# @user_passes_test(in_proj_user_group)
def share_report(request):
    if request.method == 'POST':
        shared_data_form = SharedDataForm(request.POST, instance=SharedData())
        if shared_data_form.is_valid():
            shared_data = shared_data_form.save(commit=False)
            shared_data.user = request.user
            shared_data.creation_date = datetime.date.today()
            shared_data.save()
            shared_data_form.save_m2m()
            # format the email better here TODO
            subject = 'Shared Variant Report: {}'.format(
                shared_data_form['name'].value())
            absolute_uri = request.build_absolute_uri('/')
            uuid = str(shared_data.uuid).replace('-', '')
            share_url = absolute_uri + 'viewer/shared/view/' + uuid + '/'
            recipients = [str(contact) for contact in shared_data.shared_recipient.all()]

            message = 'A variant report has been shared with you. Go to the following link to view: '
            message += share_url

            print subject
            print message

            # send_mail(subject, message, 'no-reply@uchicago.edu',
            #           recipients, fail_silently=False)

        return HttpResponseRedirect(reverse('manage_report'))
        # I don't know that we should necessarily redirect
        # Maybe just close the modal box, return to page?
        # but then how do we assure success? Or report failure? TODO
    else:
        project_pk = request.session.get('viewing_project', None)
        if project_pk is None:
            return HttpResponseRedirect(reverse('no_project'))
        report_ids = request.GET.getlist('reportid')
        reports = Report.objects.filter(pk__in=report_ids)
        shared_data_form = SharedDataForm(instance=SharedData(), initial={
            'field_lookup': simplejson.dumps({'report_id__in': report_ids})
        })
        shared_data_form.fields['shared_recipient'].queryset = Project.objects.get(pk=project_pk).contact_set.all()
        context = {
            'reports_name': ', '.join([report.name for report in reports]),
            'shared_data_form': shared_data_form
        }
        return render(request, 'viewer/share/share_report.html', context)


def zip_and_download(request):
    import zipfile
    now = datetime.datetime.now()
    zipped_name = 'VariantViewerReports_' + ''.join(map(str, [now.year, now.month, now.day, '_', now.hour,
                                                              now.minute, now.second]))
    zipped_reports = zipfile.ZipFile('viewer/files/' + zipped_name + '.zip', mode='w')

    report_ids = request.GET.getlist('reportids[]')
    report_files = [report.report_file.name for report in Report.objects.filter(pk__in=report_ids)]
    try:
        for report_file in report_files:
            zipped_reports.write('viewer/files/' + report_file, report_file)
    finally:
        zipped_reports.close()
    return HttpResponse('/viewer/files/' + zipped_name + '.zip')
