# -*- coding: utf-8 -*-
from coplay.control import post_update_to_user, user_started_a_new_discussion, \
    user_posted_a_feedback_in_another_other_user_s_discussion, \
    user_post_a_decision_for_vote_regarding_his_own_discussion, \
    string_to_email_subject, send_html_message, get_user_fullname_or_username
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task, \
    Viewer, FollowRelation, UserUpdate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from kuterless import settings
import floppyforms as forms
import kuterless.settings

MAX_MESSAGE_INPUT_CHARS = 900

def can_user_acess_discussion(discussion, user):
    if not user.is_authenticated():
        return discussion.can_user_access_discussion(None)
    
    return discussion.can_user_access_discussion(user)
        
# Create your views here.
def root(request):
    return render(request, 'coplay/co_play_root.html', {'rtl': 'dir="rtl"'})
#hi assaf
def get_discussions_lists():
    sorted_discussions_by_inverse_locket_at_list = Discussion.objects.all().order_by(
        "-locked_at")
    sorted_discussions_by_locket_at_list = Discussion.objects.all().order_by(
        "locked_at")

    active_discussions_by_urgancy_list = []
    locked_discussions_by_relevancy_list = []

    for discussion in sorted_discussions_by_inverse_locket_at_list:
        if not discussion.is_active():
            locked_discussions_by_relevancy_list.append(discussion)

    for discussion in sorted_discussions_by_locket_at_list:
        if discussion.is_active():
            active_discussions_by_urgancy_list.append(discussion)

    return active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list

class IndexView(generic.ListView):
    model = Discussion
    template_name = 'coplay/discussion_list.html'
    context_object_name = 'latest_discussion_list'


    def get_queryset(self):
        active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()
        
        all_discussions_list  = active_discussions_by_urgancy_list + locked_discussions_by_relevancy_list
        allowed_all_discussions_list = []
        for discussion in all_discussions_list:
            if can_user_acess_discussion(discussion, self.request.user):
                allowed_all_discussions_list.append(discussion)
        
        return (allowed_all_discussions_list)


class AddFeedbackForm(forms.Form):
    content = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                              widget=forms.Textarea(attrs={'rows': '3'}))
    feedbabk_type = forms.ChoiceField(choices=Feedback.FEEDBACK_TYPES)


class UpdateDiscussionForm(forms.Form):
    description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea(attrs={'rows': '3'}))


class AddDecisionForm(forms.Form):
    content = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS, label='',
                              widget=forms.Textarea(attrs={'rows': '3',
                                                           'class': 'form-control'}))


class VoteForm(forms.Form):
    value = forms.ChoiceField(widget=forms.RadioSelect,
                              choices=LikeLevel.level)


class AddTaskForm(forms.Form):
    goal_description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                       label='', widget=forms.Textarea(
            attrs={'rows': '3', 'class': 'form-control'}))
    target_date = forms.DateTimeField(widget=SelectDateWidget)


class UpdateTaskForm(forms.Form):
    status_description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                         widget=forms.Textarea(
                                             attrs={'rows': '3'}))


def discussion_details(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return HttpResponseRedirect('coplay_root')
    
    if discussion.get_is_viewing_require_login() and not request.user.is_authenticated():
        return HttpResponseRedirect( reverse('login') + '?next=' + request.path)        
    
    if not can_user_acess_discussion( discussion, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})

    list_encourage = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.ENCOURAGE).order_by("-created_at")
    list_cooperation = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.COOPERATION).order_by("-created_at")
    list_intuition = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.INTUITION).order_by("-created_at")
    list_advice = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.ADVICE).order_by("-created_at")
    list_decision = discussion.decision_set.all().order_by("-created_at")
    list_tasks = discussion.task_set.all().order_by("-target_date")
    like_levels = LikeLevel.level
    list_viewers = discussion.viewer_set.all().exclude(
        views_counter= 0 ).order_by("-views_counter_updated_at")
        
    list_anonymous_viewers = discussion.anonymousvisitorviewer_set.all().exclude(
        views_counter= 0 ).order_by("-views_counter_updated_at")

    for task in discussion.task_set.all():
        task.refresh_status()        

    list_tasks_open = discussion.task_set.all().order_by("target_date").filter(status = Task.STARTED)
    
    list_tasks_closed_and_aborted = discussion.task_set.all().exclude(status = Task.MISSED).filter(final_state = True).order_by("-closed_at")

    list_tasks = list(list_tasks_open) + list( list_tasks_closed_and_aborted)
    
    vote_form = None
    feedback_form = None
    description_form = None
    add_decision_form = None
    add_task_form = None
    is_a_follower = False
    if request.user.is_authenticated():
        if discussion.is_active():
            if request.user == discussion.owner:
                description_form = UpdateDiscussionForm()
                add_decision_form = AddDecisionForm()
            else:
                feedback_form = AddFeedbackForm()
                vote_form = VoteForm()

        add_task_form = AddTaskForm()
        is_a_follower = discussion.is_a_follower(request.user)
    else:
        vote_form = VoteForm()

    list_followers = discussion.get_followers_list()
    
    page_name = u'עוזרים ב' + discussion.title
    
    #the response shall not indicate current user's view
    return_response = render(request, 'coplay/discussion_detail.html',
                  {'discussion': discussion,
                   'list_encourage': list_encourage,
                   'list_cooperation': list_cooperation,
                   'list_intuition': list_intuition,
                   'list_advice': list_advice,
                   'list_decision': list_decision,
                   'list_tasks': list_tasks,
                   'feedback_form': feedback_form,
                   'description_form': description_form,
                   'add_decision_form': add_decision_form,
                   'vote_form': vote_form,
                   'add_task_form': add_task_form,
                   'like_levels': like_levels,
                   'list_viewers':list_viewers,
                   'list_anonymous_viewers':list_anonymous_viewers,
                   'page_name': page_name ,
                   'is_a_follower': is_a_follower,
                   'list_followers': list_followers})
    
    #current view is recorded after response had been resolved
    if request.user.is_authenticated():
        discussion.record_a_view(request.user)
    
    discussion.record_anonymous_view(request)
        
    return return_response


class NewDiscussionForm(forms.Form):
    title = forms.CharField(label=_("title"), max_length=200,
                            widget=forms.Textarea(
                                attrs={'rows': '1', 'cols': '50'}))
    description = forms.CharField(label=_("description"),
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)
    latitude    = forms.FloatField(required=False)
    longitude   = forms.FloatField(required=False)
    location_desc = forms.CharField(label=u'כתובת',
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)


@login_required
def add_discussion(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user

            discussions_list = Discussion.objects.all().filter(owner=user,
                                                               title=
                                                               form.cleaned_data[
                                                                   'title'])
            if discussions_list.count() != 0:
                return render(request, 'coplay/message.html',
                              {'message': 'כבר קיים עבורך דיון באותו נושא',
                               'rtl': 'dir="rtl"'})

            new_discussion = Discussion(owner=user,
                                        title=form.cleaned_data['title'],
                                        description=form.cleaned_data[
                                            'description'])
            latitude=form.cleaned_data['latitude']
            if latitude:
                new_discussion.latitude = latitude;
            longitude=form.cleaned_data['longitude']
            if longitude:
                new_discussion.longitude = longitude
                
            location_desc=form.cleaned_data['location_desc']
            if location_desc:
                new_discussion.location_desc = location_desc;
                
            new_discussion.clean()
            new_discussion.description_updated_at = timezone.now()
            new_discussion.save()
            messages.success(request,
                             _("Your activity was created successfully"))
            new_discussion.start_follow(user)
            
            t = Template("""
            {{discussion.owner.get_full_name|default:discussion.owner.username}} ביקש/ה את העזרה שלך ב :
            "{{discussion.title}} "\n
            """)
            
            trunkated_subject_and_detailes = t.render(Context({"discussion": new_discussion}))
                                                                
          
            discussion_email_updates(new_discussion,
                                             trunkated_subject_and_detailes,
                                             new_discussion.owner,
                                             trunkated_subject_and_detailes,
                                             mailing_list = get_followers_list(new_discussion.owner))
        
            user_started_a_new_discussion( new_discussion.owner)

            return redirect(new_discussion)
    else:
        form = NewDiscussionForm() # An unbound form

    return render(request, 'coplay/new_discussion.html', {
        'form': form,
        'rtl': 'dir="rtl"'
    })

def user_follow_start_email_updates(follower_user, following_user, inverse_following):



    t = Template("""
        {{follower_user.get_full_name|default:follower_user.username}} התחיל/ה לעקוב אחרי פתיחת הפעילויות שלך
        """)
        
    subject = t.render(Context({"follower_user": follower_user}))

    
    html_message = render_to_string("coplay/user_follow_email_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'follower_user': follower_user,
                                     'html_title': string_to_email_subject(subject),
                                     'details': subject,
                                     'inverse_following': inverse_following})
    

#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_message)
    
    if following_user.email != None and following_user.userprofile.recieve_updates:
        send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [following_user.email])

    post_update_to_user(following_user.id, 
                 header = string_to_email_subject(subject),
                 content = subject, 
                 sender_user_id = follower_user.id,  
                 details_url = reverse('coplay:user_coplay_report', kwargs={'username': follower_user}))


def discussion_email_updates(discussion, subject, logged_in_user, details = None, url_id = '', mailing_list = None):
    if mailing_list == None:
        mailing_list = discussion.get_followers_list()
    allowed_users_list = []
    for user in mailing_list:
        if discussion.can_user_access_discussion( user):
            allowed_users_list.append(user)
         
    html_message = render_to_string("coplay/email_discussion_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'discussion': discussion,
                                     'html_title': string_to_email_subject(subject),
#                                     'subject_debug':string_to_email_subject(subject),
                                     'details': details,
                                     'id': url_id})
    

#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_message)
    
    for attensdent in allowed_users_list:
        if attensdent != logged_in_user:
            if attensdent.email and attensdent.userprofile.recieve_updates:
                send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [attensdent.email])
            post_update_to_user(attensdent.id, 
                     header = string_to_email_subject(subject),
                     content = details, 
                     sender_user_id = logged_in_user.id,  
                     discussion_id = discussion.id,
                     details_url = reverse('coplay:discussion_details', kwargs={'pk': str(discussion.id)}) + url_id )


def discussion_task_email_updates(task, subject, logged_in_user, details = None):
    attending_list = task.parent.get_followers_list()
    
    allowed_users_list = []
    
    
    for user in attending_list:
        if task.parent.can_user_access_discussion( user):
            allowed_users_list.append(user)

    html_message = render_to_string("coplay/email_task_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'task': task,
                                     'html_title': string_to_email_subject(subject),
#                                     'subject_debug':string_to_email_subject(subject),
                                     'details': details})
    
#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_message)

    for attensdent in allowed_users_list:
        if attensdent != logged_in_user:
            if attensdent.email and attensdent.userprofile.recieve_updates:
                send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [attensdent.email])

            post_update_to_user(attensdent.id, 
                     header = string_to_email_subject(subject),
                     content = details, 
                     sender_user_id = logged_in_user.id,  
                     discussion_id = task.parent.id,
                     details_url = reverse('coplay:task_details', kwargs={'pk': str(task.id)}))


@login_required
def update_discussion(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'הדיון איננו קיים',
                       'rtl': 'dir="rtl"'})

    if request.method == 'POST': # If the form has been submitted...
        form = UpdateDiscussionForm(
            request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            if user == discussion.owner:
                discussion.update_description(
                    form.cleaned_data['description'])
                discussion_email_updates(discussion,
                                         'עידכון מטרות בפעילות שבהשתתפותך',
                                         request.user)

                return HttpResponseRedirect(
                    discussion.get_absolute_url()) # Redirect after POST
            return render(request, 'coplay/message.html',
                          {'message': 'רק בעל הדיון מורשה לעדכן אותו',
                           'rtl': 'dir="rtl"'})

    return render(request, 'coplay/message.html',
                  {'message': '  לא הוזן תיאור חדש או שהוזן תיאור ארוך מדי ',
                   'rtl': 'dir="rtl"'})


@login_required
def delete_discussion(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'הדיון איננו קיים',
                       'rtl': 'dir="rtl"'})

    user = request.user
    if user == discussion.owner:
        discussion.delete()
        return HttpResponseRedirect(
            'discussions_list') # Redirect to discussions list

    return render(request, 'coplay/message.html',
                  {'message': 'רק בעל הדיון  מורשה למחוק אותו',
                   'rtl': 'dir="rtl"'})


@login_required
def start_follow(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return HttpResponseRedirect('coplay_root')
    
    if not can_user_acess_discussion( discussion, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})
    
    discussion.start_follow(request.user)
    
    return discussion_details(request, pk)    
    
@login_required
def stop_follow(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return HttpResponseRedirect('coplay_root')
    
    
    if not can_user_acess_discussion( discussion, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})
    
    
    
    discussion.stop_follow(request.user)
    
    return HttpResponseRedirect(
                discussion.get_absolute_url())    
    

@login_required
def add_feedback(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddFeedbackForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            if user != discussion.owner and form.cleaned_data[
                'feedbabk_type'] and form.cleaned_data['content']:
                feedback = discussion.add_feedback(user,
                                        form.cleaned_data['feedbabk_type'],
                                        form.cleaned_data['content'])
                subject_text = u""
                
                discussion_email_updates(discussion,
                                         'התקבלה תגובה חדשה בפעילות שבהשתתפותך',
                                         request.user)

            return HttpResponseRedirect(
                discussion.get_absolute_url()) # Redirect after POST
        return render(request, 'coplay/message.html',
                      {'message': 'לא הזנת תגובה',
                       'rtl': 'dir="rtl"'})
    return HttpResponse('Request NA')


@login_required
def add_decision(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddDecisionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            user = request.user
            if user == discussion.owner:
                decisions_list = Decision.objects.all().filter(
                    content=form.cleaned_data['content'], parent=discussion)
                if decisions_list.count() != 0:
                    return render(request, 'coplay/message.html',
                                  {
                                      'message': 'כבר רשומה עבורך החלטה באותו נושא',
                                      'rtl': 'dir="rtl"'})

                discussion.add_decision(form.cleaned_data['content'])
                discussion_email_updates(discussion,
                                         'התקבלה התלבטות חדשה בפעילות שבהשתתפותך',
                                         request.user)



            else:
                return HttpResponse('Forbidden access')
            return HttpResponseRedirect(
                discussion.get_absolute_url()) # Redirect after POST
        else:
            return render(request, 'coplay/message.html',
                          {'message': 'בחר אחת מהאפשרויות',
                           'rtl': 'dir="rtl"'})
    return HttpResponseRedirect('coplay_root') # Redirect after POST


@login_required
def vote(request, pk):
    try:
        decision = Decision.objects.get(id=int(pk))
    except Decision.DoesNotExist:
        return render(request, 'coplay/message.html',
                              {'message': 'משימה לא ידועה',
                               'rtl': 'dir="rtl"'})
        
    if not can_user_acess_discussion( decision.parent, request.user):
        return render(request, 'coplay/message.html', 
                                  {  'message'      :  'אינך מורשה לצפות בדיון',
                                   'rtl': 'dir="rtl"'})    
    
    
    
    
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            if user != decision.parent.owner:
                decision.vote(user, int(form.cleaned_data['value']))
                decision.parent.start_follow(user)

            return HttpResponseRedirect(
                decision.get_absolute_url()) # Redirect after POST
        return render(request, 'coplay/message.html',
                      {'message': 'Please select a vote value'})

    return ( HttpResponse('Forbidden request not via form'))


@login_required
def add_task(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            target_date = form.cleaned_data['target_date']
            if target_date <= timezone.now():
                return render(request, 'coplay/message.html',
                              {'message': 'תאריך היעד חייב להיות בעתיד' + str(
                                  target_date),
                               'rtl': 'dir="rtl"'})

            tasks_list = Task.objects.all().filter(responsible=user,
                                                   goal_description=
                                                   form.cleaned_data[
                                                       'goal_description'],
                                                   parent=discussion)
            if tasks_list.count() != 0:
                return render(request, 'coplay/message.html',
                              {'message': 'כבר רשומה עבורך משימה באותו נושא',
                               'rtl': 'dir="rtl"'})

            new_task = discussion.add_task(user,
                                           form.cleaned_data[
                                               'goal_description'],
                                           form.cleaned_data['target_date'])

            discussion_task_email_updates(new_task,
                                          'נוספה משימה חדשה בפעילות שבהשתתפותך',
                                          request.user)

            return HttpResponseRedirect(
                new_task.get_absolute_url()) # Redirect after POST

    return HttpResponseRedirect('coplay_root') # Redirect after POST


def task_details(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'משימה שאיננה קיימת',
                       'rtl': 'dir="rtl"'})
        
    if not can_user_acess_discussion( task.parent, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})

    close_possible = False
    update_task_form = None

    if request.user.is_authenticated():
        user = request.user
        if  task.target_date > timezone.now():
            if user == task.responsible:
                update_task_form = UpdateTaskForm(initial={'status_description': task.status_description})
            else:
                close_possible = True

    return render(request, 'coplay/task_detail.html',
                  {'task': task,
                   'update_task_form': update_task_form,
                   'close_possible': close_possible,
                   'rtl': 'dir="rtl"',
                   'page_name': u'המשימה:' + task.goal_description})


@login_required
def update_task_description(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = UpdateTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                task = Task.objects.get(id=int(pk))
            except Task.DoesNotExist:
                return HttpResponse('Task not found')
            user = request.user
            if user == task.responsible:
                task.update_status_description(
                    form.cleaned_data['status_description'])
                task.parent.save()#verify that the entire disscusion is considered updated
                t = Template("""
                {{task.responsible.get_full_name|default:task.responsible.username}} הודיע/ה ש :\n
                "{{task.get_status_description}} "\n
                """)
                
                trunkated_subject_and_detailes = t.render(Context({"task": task}))
                
                discussion_task_email_updates(task,
                                              trunkated_subject_and_detailes,
                                              request.user,
                                              trunkated_subject_and_detailes)
                
                

            return HttpResponseRedirect(
                task.parent.get_absolute_url()) # Redirect after POST

    return HttpResponseRedirect('coplay_root') # Redirect after POST

def task_state_change_update(task, state_change_description):
    t = Template("""
                {{task.responsible.get_full_name|default:task.responsible.username}} {{state_change_description}} :\n
                 "{{task.goal_description}} "\nאושר על ידי {{task.closed_by.get_full_name|default:task.closed_by.username}}
                 """)
                
    trunkated_subject_and_detailes = t.render(Context({"task": task, 'state_change_description': state_change_description}))


                
    discussion_task_email_updates(task,
                                    trunkated_subject_and_detailes,
                                    task.closed_by,
                                    trunkated_subject_and_detailes)


@login_required
def close_task(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    
    if not can_user_acess_discussion( task.parent, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})
    
    user = request.user
    if user != task.responsible:
        if task.close(user):
            task.parent.save() #verify that the entire discussion is considered updated            
            task_state_change_update( task,  u" השלימ/ה את ")


    return HttpResponseRedirect(task.parent.get_absolute_url()) # Redirect after POST


@login_required
def abort_task(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    
    if not can_user_acess_discussion( task.parent, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})
    
    
    user = request.user
    if user != task.responsible:
        if task.abort(user):
            task.parent.save() #verify that the entire discussion is considered updated            
            task_state_change_update( task,  u" ביטל/ה את ")

    return HttpResponseRedirect(task.parent.get_absolute_url()) # Redirect after POST


@login_required
def re_open_task(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    
    if not can_user_acess_discussion( task.parent, request.user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בדיון',
                       'rtl': 'dir="rtl"'})
    
    user = request.user
    if user != task.responsible:
        if task.re_open(user):
            task.parent.save() #verify that the entire discussion is considered updated            
            task_state_change_update( task,  u" עדיין לא השלים/ה את ")


    return HttpResponseRedirect(task.parent.get_absolute_url()) # Redirect after POST



def get_tasks_lists():
    for task in Task.objects.all():
        task.refresh_status()
    open_tasks_list_by_urgancy_list = Task.objects.all().filter(
        status=Task.STARTED).order_by("target_date")
    closed_tasks_list_by_relevancy_list = Task.objects.all().filter(
        status=Task.CLOSED).order_by("-closed_at")
    missed_tasks_list_by_relevancy_list = Task.objects.all().filter(
        status=Task.MISSED).order_by("-target_date")

    return open_tasks_list_by_urgancy_list, closed_tasks_list_by_relevancy_list, missed_tasks_list_by_relevancy_list



def user_coplay_report(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('User not found')        
    else:
        user = request.user
        
    if  request.user.is_authenticated():
        viewer_user = request.user
        if  not  user.userprofile.is_in_the_same_segment(request.user):
            return render(request, 'coplay/message.html', 
                      {  'message'      :  'משתמש ממודר',
                       'rtl': 'dir="rtl"'})
    else:
        viewer_user = None
        if user.userprofile.get_segment():
            return render(request, 'coplay/message.html', 
                      {  'message'      :  'משתמש ממודר',
                       'rtl': 'dir="rtl"'})

    if user == request.user:
        page_name = u'הפעילות שלי '
    else:
        page_name = u'הפעילות של ' + get_user_fullname_or_username(user)

    open_tasks_list_by_urgancy_list, closed_tasks_list_by_relevancy_list, missed_tasks_list_by_relevancy_list = get_tasks_lists()

    active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()

    user_s_open_tasks_list = []
    other_users_open_tasks_list = []
    failed_tasks_list = []
    user_closed_tasks_list = []

    for task in open_tasks_list_by_urgancy_list:  
        if task.parent.can_user_access_discussion(viewer_user):      
            if task.responsible == user:
                user_s_open_tasks_list.append(task)
            else:
                discussion = task.parent
                if user in discussion.get_followers_list():
                    other_users_open_tasks_list.append(task)
                
    tasks_by_recent_closed_at_date = Task.objects.all().exclude(status = task.MISSED).order_by("-closed_at")

    for task in tasks_by_recent_closed_at_date:
        discussion = task.parent
        if user in discussion.get_followers_list() and discussion.can_user_access_discussion(viewer_user):
            status = task.get_status()
            if status == Task.ABORTED:
                failed_tasks_list.append(task)

    number_of_closed_tasks_for_others = 0
    for task in closed_tasks_list_by_relevancy_list:
        if task.responsible == user:
            user_closed_tasks_list.append(task)
            if task.parent.owner != user:
                number_of_closed_tasks_for_others +=1

    user_discussions_active = []
    user_discussions_locked = []

    for discussion in active_discussions_by_urgancy_list:
        if user in discussion.get_followers_list() and discussion.can_user_access_discussion(viewer_user):
            user_discussions_active.append(discussion)

    for discussion in locked_discussions_by_relevancy_list:
        if user in discussion.get_followers_list() and discussion.can_user_access_discussion(viewer_user):
            user_discussions_locked.append(discussion)
            
    number_of_closed_tasks = len(user_closed_tasks_list)
    

    number_of_views = 0
    views_list = Viewer.objects.filter( user = user)
    for view in views_list:
        if view.discussion.owner != user:
            number_of_views += view.get_views_counter()
    
    number_of_feedbacks = user.feedback_set.all().count()
    number_of_votes     = user.vote_set.all().count()
    number_of_task_closing = Task.objects.filter( closed_by = user ).count()
    number_of_aborted_tasks = Task.objects.filter( status=Task.ABORTED, responsible = user ).count()
    
    followers_list = get_followers_list(user)
    following_list = get_following_list(user)
    if request.user.is_authenticated():
        is_following = is_user_is_following(request.user, user)
    else:
        is_following = False
        
    user_updates_query_set = user.recipient.all().order_by("-created_at")
    user_updates_that_viewer_can_access_list = []
    
    for user_update in user_updates_query_set:
        if user_update.can_user_access(viewer_user):
            user_updates_that_viewer_can_access_list.append(user_update)
            
    return render(request, 'coplay/coplay_report.html',
                  {
                      'number_of_closed_tasks'           : number_of_closed_tasks,
                      'number_of_closed_tasks_for_others': number_of_closed_tasks_for_others,
                      'number_of_aborted_tasks'          : number_of_aborted_tasks,
                      'number_of_task_closing'           : number_of_task_closing,
                      'number_of_views'                  : number_of_views       ,
                      'number_of_feedbacks'              : number_of_feedbacks   ,
                      'number_of_votes'                  : number_of_votes       ,
                      'user_updates_that_viewer_can_access_list': user_updates_that_viewer_can_access_list,
                      'tasks_open_by_increased_time_left': user_s_open_tasks_list,
                      'tasks_others_open_by_increased_time_left': other_users_open_tasks_list,
                      'discussions_active_by_increase_time_left': user_discussions_active,
                      'discussions_locked_by_increase_locked_at': user_discussions_locked,
                      'tasks_closed_by_reverse_time': user_closed_tasks_list,
                      'tasks_failed_by_reverse_update_time': failed_tasks_list,
                      'applicabale_user': user,
                      'followers_list' :followers_list,
                      'following_list' :following_list,
                      'is_following'   :is_following,
                      'page_name': page_name,
                      'description': user.userprofile.description,
                      'location_desc': user.userprofile.location_desc})


class UpdateDiscussionDescForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = (
            'description',
            'latitude',  
            'longitude',
            'location_desc', 
        )


class DiscussionOwnerView(object):
    model = Discussion

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = self.get_object()
        if self.discussion.owner != request.user:
            return HttpResponse("Unauthorized", status=401)
        
        return super(DiscussionOwnerView, self).dispatch(request, *args,
                                                              **kwargs)

class UpdateDiscussionDescView(DiscussionOwnerView, UpdateView):
    
    form_class = UpdateDiscussionDescForm
    
    def form_valid(self, form):

        resp = super(UpdateDiscussionDescView, self).form_valid(form)  
        form.instance.description_updated_at = timezone.now()
        form.instance.save()

        

        t = Template("""
        {{discussion.owner.get_full_name|default:discussion.owner.username}} עידכן/ה את המטרות של הפעילות והעזרה המבוקשת :\n
        "{{discussion.description}} "\n
        """)
        
        trunkated_subject_and_detailes = t.render(Context({"discussion": form.instance}))
                                                            
      
        discussion_email_updates(form.instance,
                                         trunkated_subject_and_detailes,
                                         self.request.user,
                                         trunkated_subject_and_detailes)
        form.instance.start_follow(self.request.user)
        
        return resp
    


class DeleteDiscussionView(DiscussionOwnerView, DeleteView):

    model = Discussion


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'goal_description',
            'target_date',
        )
        widgets = {
            'goal_description': forms.Textarea,
            'target_date': forms.DateInput,
        }

class CreateTaskView(CreateView):
    model = Task
    form_class = CreateTaskForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        return super(CreateTaskView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        if form.instance.target_date <= timezone.now():
            return render(self.request, 'coplay/message.html',
                              {'message': 'תאריך היעד חייב להיות בעתיד' + str(
                                  form.instance.target_date),
                               'rtl': 'dir="rtl"'})
        form.instance.parent = self.discussion
        form.instance.responsible = self.request.user
        if Task.objects.filter( parent = self.discussion,  responsible = form.instance.responsible,  goal_description = form.instance.goal_description).exists():
            task = Task.objects.get( goal_description = form.instance.goal_description)
            return HttpResponseRedirect(
                    task.get_absolute_url())
        resp = super(CreateTaskView, self).form_valid(form)
        form.instance.parent.save() #verify that the entire discussion is considered updated
        form.instance.parent.unlock()
        

        t = Template("""
        {{task.responsible.get_full_name|default:task.responsible.username}} הבטיח/ה ש :\n
        "{{task.goal_description}} "\n  עד {{task.target_date | date:"d/n/Y H:i"}}
        """)
        
        trunkated_subject_and_detailes = t.render(Context({"task": form.instance}))
      
        discussion_task_email_updates(form.instance,
                                         trunkated_subject_and_detailes,
                                         self.request.user,
                                         trunkated_subject_and_detailes)
        
        self.discussion.start_follow(self.request.user)
        
        
        return resp


class CreateFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            'feedbabk_type',
            'content',
        )
        widgets = {
            'content': forms.Textarea,
            'feedbabk_type': forms.Select,
        }



class CreateFeedbackView(CreateView):
    model = Feedback
    form_class = CreateFeedbackForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        if self.discussion.owner == request.user:
            return HttpResponse("Unauthorized", status=401)
        
        return super(CreateFeedbackView, self).dispatch(request, *args,
                                                              **kwargs)


    def form_valid(self, form):
        form.instance.discussion = self.discussion
        form.instance.user = self.request.user
        if Feedback.objects.filter( discussion = self.discussion, feedbabk_type = form.instance.feedbabk_type, content = form.instance.content).exists():
            return HttpResponseRedirect(
                    self.discussion.get_absolute_url())
            
        resp = super(CreateFeedbackView, self).form_valid(form)  
        form.instance.discussion.save() #verify that the entire discussion is considered updated

        t = Template("""
        {{feedbabk.user.get_full_name|default:feedbabk.user.username}} פירסם/ה {{feedbabk.get_feedbabk_type_name}}:\n
        "{{feedbabk.content}} "\n
        """)

        trunkated_subject_and_detailes = t.render(Context({"feedbabk": form.instance}))
        
                                                            
                                                            
        discussion_email_updates(form.instance.discussion,
                                         trunkated_subject_and_detailes,
                                         self.request.user,
                                         trunkated_subject_and_detailes)
        
        form.instance.discussion.start_follow(self.request.user)
        
        user_posted_a_feedback_in_another_other_user_s_discussion(form.instance.user, form.instance.get_absolute_url())

        
        return resp


class CreateDecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea,
        }



class CreateDecisionView(CreateView):
    model = Decision
    form_class = CreateDecisionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        if self.discussion.owner != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(CreateDecisionView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        form.instance.parent = self.discussion
        if Decision.objects.filter( parent = self.discussion, content = form.instance.content).exists():
            return HttpResponseRedirect(
                    self.discussion.get_absolute_url())
        resp = super(CreateDecisionView, self).form_valid(form)
        form.instance.parent.save() #verify that the entire discussion is considered updated
        
        # form.instance is the new decision
        

        t = Template("""
        {{decision.parent.owner.get_full_name|default:decision.parent.owner.username}} מבקש/ת שתצביע/י על :\n
        "{{decision.content}} "\nלהצבעה צריך להיכנס אל הפעילות המלאה...
        """)
        
        trunkated_subject_and_detailes = t.render(Context({"decision": form.instance}))
                                                            
      
        
        discussion_email_updates(form.instance.parent,
                                         trunkated_subject_and_detailes,
                                         self.request.user,
                                         trunkated_subject_and_detailes,
                                         "#Decisions")
        
        form.instance.parent.start_follow(self.request.user)
        
        user_post_a_decision_for_vote_regarding_his_own_discussion( form.instance.parent.owner, form.instance.get_absolute_url())

        return resp

def get_followers_list( following_user):
    
    followers_list = []
    
    follow_relations_set = FollowRelation.objects.filter( following_user = following_user)
    
    for follow_relations in follow_relations_set:
        followers_list.append(follow_relations.follower_user)
        
    return followers_list

def get_following_list( follower_user):
    
    following_list = []
    
    follow_relations_set = FollowRelation.objects.filter( follower_user = follower_user)
    
    for follow_relations in follow_relations_set:
        following_list.append(follow_relations.following_user)
        
    return following_list


    
def is_user_is_following( follower_user, following_user):
    return FollowRelation.objects.filter( follower_user = follower_user, following_user = following_user).exists()

def start_users_following( follower_user, following_user):
    
    if follower_user == following_user:
        return
    

    already_following = is_user_is_following( follower_user, following_user)
    
    inverse_following = is_user_is_following(following_user ,  follower_user )

    FollowRelation.objects.get_or_create( follower_user = follower_user, following_user = following_user)
    
    if not already_following:
        user_follow_start_email_updates(follower_user, following_user, inverse_following)
     

def stop_users_following( follower_user, following_user):
    if FollowRelation.objects.filter( follower_user = follower_user, following_user = following_user).exists():
        deleted_follow_relation = FollowRelation.objects.get( follower_user = follower_user, following_user = following_user) 
        deleted_follow_relation.delete()
            

@login_required
def start_follow_user(request, username):
    try:
        following_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'לא נמצא',
                       'rtl': 'dir="rtl"'})
    
    
    if not request.user.userprofile.is_in_the_same_segment(following_user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'משתמש ממודר',
                       'rtl': 'dir="rtl"'})
        
    
    
    start_users_following( request.user, following_user)
    
    return HttpResponseRedirect(reverse('coplay:user_coplay_report', kwargs={'username': following_user}))

@login_required
def stop_follow_user(request, username):
    try:
        following_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'לא נמצא',
                       'rtl': 'dir="rtl"'})
    
    stop_users_following( request.user, following_user)
        
    return HttpResponseRedirect(reverse('coplay:user_coplay_report', kwargs={'username': following_user}))

def user_update_details(request, pk):
    try:
        user_update = UserUpdate.objects.get(id=int(pk))
    except UserUpdate.DoesNotExist:
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'לא נמצא',
                       'rtl': 'dir="rtl"'})
    
    if request.user.is_authenticated():
        viewing_user = request.user
    else:
        viewing_user = None
        
    if not user_update.can_user_access(viewing_user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בעדכון',
                       'rtl': 'dir="rtl"'})
    
    render_result = render(request, 'coplay/user_update_detailes.html', 
                      {  'user_update'      :  user_update,
                       'rtl': 'dir="rtl"'})
    
    if viewing_user == user_update.recipient:
        user_update.set_as_already_read()
        
    
    return render_result


def user_update_mark_recipient_read(request, pk):
    try:
        user_update = UserUpdate.objects.get(id=int(pk))
    except UserUpdate.DoesNotExist:
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'לא נמצא',
                       'rtl': 'dir="rtl"'})
    
    if request.user.is_authenticated():
        viewing_user = request.user
    else:
        viewing_user = None
        
    if not user_update.can_user_access(viewing_user):
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'אינך מורשה לצפות בעדכון',
                       'rtl': 'dir="rtl"'})


        
    redirect_to = user_update.details_url
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = 'home'        
        
    if viewing_user == user_update.recipient:
        user_update.set_as_already_read()
        
        
    return HttpResponseRedirect(redirect_to) # Redirect after POST
    
    