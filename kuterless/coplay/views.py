# -*- coding: utf-8 -*-
from coplay.control import get_discussions_lists, get_tasks_lists
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task, \
    Viewer, UserUpdate, MAX_TEXT
from coplay.services import update_task_status_description, update_task_state, \
    start_users_following, stop_users_following, start_tag_following, \
    stop_tag_following, create_discussion, discussion_add_task, decision_vote, \
    discussion_record_a_view, discussion_record_anonymous_view, \
    discussion_add_decision, discussion_add_feedback, get_user_fullname_or_username, \
    get_followers_list, get_following_list, is_user_is_following, \
    poll_for_task_complition, discussion_update, can_user_acess_discussion, \
    is_in_the_same_segment, task_get_status, start_discussion_following, \
    stop_discussion_following, MAX_MESSAGE_INPUT_CHARS, \
    get_discussion_with_parent_url_list
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import request
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.base import Template
from django.template.context import Context
from django.template.defaultfilters import pprint
from django.utils import six, timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from kuterless.settings import SITE_URL, MEDIA_URL
from taggit.forms import TagField
from taggit.models import Tag
from taggit.utils import edit_string_for_tags
import floppyforms as forms
import sys



        

class TagWidgetBig(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, six.string_types):
            value = edit_string_for_tags([
                o.tag for o in value.select_related("tag")])
        return super(TagWidgetBig, self).render(name, value, attrs)
        
# Create your views here.
def root(request):
    if( request.user.is_authenticated()):
        return HttpResponseRedirect(reverse('coplay:user_coplay_report', kwargs={'username': request.user.username}))        
    return render(request, 'coplay/co_play_root.html', {'rtl': 'dir="rtl"'})

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
    
    voice_recording = forms.FileField(required=False)

class UpdateDiscussionForm(forms.Form):
    description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                  label = u'תאור הפעילות' , help_text = u'תאור היעד ואיזו עזרה מבוקשת', widget=forms.Textarea(attrs={'rows': '3',
                                     'cols' : '40'}))
    m_tags = TagField(required=False, label = 'תגיות' , help_text = u'רשימה של תגים מופרדת עם פסיקים.', widget=forms.Textarea(attrs={'rows': '3',
                                     'cols' : '40'}))


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
    
    result_picture = forms.ImageField(required=False)

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
    for task in list_tasks:
        poll_for_task_complition(task)
    like_levels = LikeLevel.level
    list_viewers = discussion.viewer_set.all().exclude(
        views_counter= 0 ).order_by("-views_counter_updated_at")
        
    list_anonymous_viewers = discussion.anonymousvisitorviewer_set.all().exclude(
        views_counter= 0 ).order_by("-views_counter_updated_at")

    list_tasks_open = discussion.task_set.all().order_by("target_date").filter(status = Task.STARTED)
    
#     list_tasks_closed_and_aborted = discussion.task_set.all().exclude(status = Task.MISSED).filter(final_state = True).order_by("-closed_at")
    list_tasks_closed_and_aborted = discussion.task_set.all().exclude(status = Task.MISSED).order_by("-updated_at")

    list_tasks = list(list_tasks_open) + list( list_tasks_closed_and_aborted)
    
    vote_form = None
    feedback_form = None
    description_form = None
    add_decision_form = None
    add_task_form = None

    is_a_follower = discussion.is_a_follower(request.user)
    
    add_task_form = AddTaskForm()        
    if request.user == discussion.owner:
        if discussion.is_active():
            description_form = UpdateDiscussionForm()
            add_decision_form = AddDecisionForm()
    else:
        vote_form = VoteForm()
        feedback_form = AddFeedbackForm()
 
    list_followers = discussion.get_followers_list()
    
    page_name = u'עוזרים ב' + discussion.title
    
    applicabale_discussions_list, list_title = get_discussion_with_parent_url_list( request.path, request.user)

    
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
                   'list_followers': list_followers,
                   'related_discussions': applicabale_discussions_list != [],
                   'ROOT_URL': 'http://' + SITE_URL})
    
    #current view is recorded after response had been resolved
    if request.user.is_authenticated():
        success, error_string = discussion_record_a_view (discussion, request.user)
        if success == False:
            return render(request, 'coplay/message.html', 
                      {  'message'      :  error_string,
                       'rtl': 'dir="rtl"'})

    discussion_record_anonymous_view (discussion, request)
            
    return return_response


class NewDiscussionForm(forms.Form):
    title = forms.CharField(label=_("title"), max_length=200,
                            widget=forms.Textarea(
                                attrs={'rows': '1', 'cols': '100'}))
    description = forms.CharField(label=_("description"),
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea(
                                attrs={'rows': '6', 'cols': '100'}))
    location_desc = forms.CharField(label=u'כתובת',required=False,
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea(
                                attrs={'rows': '1', 'cols': '100'}))
    
    tags = forms.CharField( required=False, label=u'תגיות מופרדות בפסיקים', widget = TagWidgetBig(attrs={'rows': 3 ,'cols' : 40} )  )


#     parent_url = forms.URLInput(label=u"דף קשור", max_length=200,
#                             widget=forms.Textarea(
#                                 attrs={'rows': '1', 'cols': '100'}))
    parent_url = forms.URLField(label=u'קישור לדף רלוונטי. לדוגמה http://hp.com',
                                required=False,
                                max_length=MAX_TEXT)
    
    parent_url_text = forms.CharField(  label=u"שם הדף הקשור", 
                                        required=False,
                                        max_length=MAX_TEXT,
                                        widget=forms.Textarea(
                                            attrs={'rows': '1', 'cols': '100'}))
    
    picture = forms.ImageField(required=False)

@login_required
def add_discussion(request, pk = None):

    use_template = 'coplay/new_discussion.html'
#     if add_on:
#         use_template = 'coplay/add_on_new_discussion.html'
    
    
    if request.method == 'POST': # If the form has been submitted...
        form = NewDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            new_discussion, error_string = create_discussion( user      = request.user, 
                                                       title            = form.cleaned_data['title'], 
                                                       description      = form.cleaned_data['description'],                       
                                                       location_desc    = form.cleaned_data['location_desc'],
                                                       tags_string      = form.cleaned_data['tags'],
                                                       parent_url       = form.cleaned_data['parent_url'],
                                                       parent_url_text  = form.cleaned_data['parent_url_text'],
                                                       picture          = form.cleaned_data['picture'])
            
            if new_discussion:
                messages.success(request,_("Your activity was created successfully"))
                return redirect(new_discussion)
                
            messages.error(request, error_string)
    else:
        parent_url = request.REQUEST.get('parent_url', '')
        parent_url_text = request.REQUEST.get('parent_url_text', '')
        if parent_url:
            form = NewDiscussionForm(initial={'parent_url': parent_url,
                                              'parent_url_text': parent_url_text}) # An unbound form
            return render(request, use_template, {
                'form': form,
                'rtl': 'dir="rtl"'
            })
            
        if pk:
            try:
                tag = Tag.objects.get(id=int(pk))
            except Tag.DoesNotExist:
                return render(request, 'coplay/message.html',
                              {'message': 'הנושא איננו קיים',
                               'rtl': 'dir="rtl"'})
            form = NewDiscussionForm(initial={'tags': tag.name}) # An unbound form
            request.user.userprofile.followed_discussions_tags.add( tag.name)
            request.user.userprofile.save()
        else:
            form = NewDiscussionForm() # An unbound form

        
    return render(request, use_template, {
        'form': form,
        'rtl': 'dir="rtl"'
    })



@login_required
def add_on_add_discussion(request, pk = None):
    
    
    use_template = 'coplay/add_on_new_discussion.html'
    
    if request.method == 'POST': # If the form has been submitted...
        form = NewDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            new_discussion, error_string = create_discussion( user             = request.user, 
                                                       title            = form.cleaned_data['title'], 
                                                       description      = form.cleaned_data['description'],                       
                                                       location_desc    = form.cleaned_data['location_desc'],
                                                       tags_string      = form.cleaned_data['tags'],
                                                       parent_url       = form.cleaned_data['parent_url'],
                                                       parent_url_text  = form.cleaned_data['parent_url_text'])
            
            if new_discussion:
                messages.success(request,_("Your activity was created successfully"))
                return redirect(new_discussion)
                
            messages.error(request, error_string)
    else:
        parent_url = request.REQUEST.get('parent_url', '')
        parent_url_text = request.REQUEST.get('parent_url_text', '')
        if parent_url:
            form = NewDiscussionForm(initial={'parent_url': parent_url,
                                              'parent_url_text': parent_url_text}) # An unbound form
            return render(request, use_template, {
                'form': form,
                'rtl': 'dir="rtl"'
            })
            
        if pk:
            try:
                tag = Tag.objects.get(id=int(pk))
            except Tag.DoesNotExist:
                return render(request, 'coplay/message.html',
                              {'message': 'הנושא איננו קיים',
                               'rtl': 'dir="rtl"'})
            form = NewDiscussionForm(initial={'tags': tag.name}) # An unbound form
            request.user.userprofile.followed_discussions_tags.add( tag.name)
            request.user.userprofile.save()
        else:
            form = NewDiscussionForm() # An unbound form


    data = render(request, use_template, {
            'form': form,
            'rtl': 'dir="rtl"'
        })
    response = HttpResponse(data)
    response['X-Frame-Options'] = "ALLOWALL"
    return response

#         
#     return render(request, use_template, {
#         'form': form,
#         'rtl': 'dir="rtl"'
#     })
 
# @login_required
# def update_discussion(request, pk):
#     try:
#         discussion = Discussion.objects.get(id=int(pk))
#     except Discussion.DoesNotExist:
#         return render(request, 'coplay/message.html',
#                       {'message': 'הדיון איננו קיים',
#                        'rtl': 'dir="rtl"'})
# 
#     if request.method == 'POST': # If the form has been submitted...
#         form = UpdateDiscussionForm(
#             request.POST) # A form bound to the POST data
#         if form.is_valid(): # All validation rules pass
#             # Process the data in form.cleaned_data# Process the data in form.cleaned_data
#             user = request.user
#             if user == discussion.owner:
#                 discussion.update_description(
#                     form.cleaned_data['description'])
#                 discussion_email_updates(discussion,
#                                          'עידכון מטרות בפעילות שבהשתתפותך',
#                                          request.user)
# 
#                 return HttpResponseRedirect(
#                     discussion.get_absolute_url()) # Redirect after POST
#             return render(request, 'coplay/message.html',
#                           {'message': 'רק בעל הדיון מורשה לעדכן אותו',
#                            'rtl': 'dir="rtl"'})
#     else:
#         form = UpdateDiscussionForm(initial={'m_tags': form.instance.tag}) # An unbound form
# 
#     return render(request, 'coplay/message.html',
#                   {'message': '  לא הוזן תיאור חדש או שהוזן תיאור ארוך מדי ',
#                    'rtl': 'dir="rtl"'})


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
    
    start_discussion_following( discussion, request.user)
    
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
    
    
    
    stop_discussion_following( discussion, request.user)
    
    return HttpResponseRedirect(
                discussion.get_absolute_url())    
    



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
            success, error_string = decision_vote( decision, request.user, int(form.cleaned_data['value']))
            if success == False:
                return render(request, 'coplay/message.html',
                      {'message': error_string})
                
            return HttpResponseRedirect(
                decision.get_absolute_url()) # Redirect after POST

    return ( HttpResponse('Forbidden request not via form'))

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
                update_task_form = UpdateTaskForm(initial={'status_description': task.status_description,
                                                           'result_picture': task.result_picture})
            else:
                close_possible = True

    return render(request, 'coplay/task_detail.html',
                  {'task': task,
                   'update_task_form': update_task_form,
                   'close_possible': close_possible,
                   'rtl': 'dir="rtl"',
                   'page_name': u'המשימה:' + task.goal_description,
                   'ROOT_URL': 'http://' + SITE_URL})


@login_required
def update_task_description(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    if request.method == 'POST': # If the form has been submitted...
        form = UpdateTaskForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            success, error_string =   update_task_status_description(   task, 
                                                                        description = form.cleaned_data['status_description'], 
                                                                        user = request.user,
                                                                        result_picture = form.cleaned_data['result_picture'])
            
            if success:
                return HttpResponseRedirect(
                    task.get_absolute_url()) # Redirect after POST
                
            return render(request, 'coplay/message.html',
                                          {'message': error_string,
                                           'rtl': 'dir="rtl"',
                                           'next_url':task.get_absolute_url(),
                                           'next_text': u'בחזרה ל:' + task.goal_description})            

        
    return HttpResponseRedirect(
                    task.parent.get_absolute_url()) # Redirect after POST

@login_required
def add_feedback(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return HttpResponse('Discussion not found')
    if request.method == 'POST': # If the form has been submitted...
        form = AddFeedbackForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
    #         if Feedback.objects.filter( discussion = self.discussion, feedbabk_type = form.instance.feedbabk_type, content = form.instance.content).exists():
    #             return HttpResponseRedirect(
    #                     self.discussion.get_absolute_url())
                
    #         resp = super(CreateFeedbackView, self).form_valid(form) 
             
            feedback, error_string = discussion_add_feedback( discussion    = discussion, 
                                                             user           = request.user   ,
                                                             feedbabk_type  = form.cleaned_data['feedbabk_type'], 
                                                             content        = form.cleaned_data['content'],
                                                             voice_recording = form.cleaned_data['voice_recording'])
            
            if feedback:
                return HttpResponseRedirect(
                    discussion.get_absolute_url()) # Redirect after POST
                
            return render(request, 'coplay/message.html',
                                          {'message': error_string,
                                           'rtl': 'dir="rtl"',
                                           'next_url':discussion.get_absolute_url(),
                                           'next_text': u'בחזרה ל:' + discussion.title})            

        
    return HttpResponseRedirect(
                    discussion.get_absolute_url()) # Redirect after POST


def set_task_state(request, pk, new_state):
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
        updated_task, error_string = update_task_state( task, 
                                                        new_state = new_state, 
                                                        user = user)
        
        if updated_task == None:
            return render(request, 'coplay/message.html',
              {'message': error_string,
               'rtl': 'dir="rtl"',
               'next_url' : task.parent.get_absolute_url(),
               'next_text'  : u"חזרה לפעילות"})


    return HttpResponseRedirect(task.parent.get_absolute_url()) # Redirect after POST

@login_required
def close_task(request, pk):
    return set_task_state( request, pk, Task.CLOSED)


@login_required
def abort_task(request, pk):
    return set_task_state( request, pk, Task.ABORTED)


@login_required
def re_open_task(request, pk):
    return set_task_state( request, pk, Task.STARTED)




def user_coplay_report(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('User not found')        
    else:
        user = request.user
        
    if not is_in_the_same_segment( user, request.user):
        return render(request, 'coplay/message.html', 
                  {  'message'      :  'משתמש ממודר',
                   'rtl': 'dir="rtl"'})

    if user == request.user:
        page_name = u'הפעילות שלי '
    else:
        page_name = u'הפעילות של ' + get_user_fullname_or_username(user)

    open_tasks_list_by_urgancy_list, closed_tasks_list_by_relevancy_list, aborted_tasks_list_by_relevancy_list , missed_tasks_list_by_relevancy_list = get_tasks_lists()

    active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()

    user_s_open_tasks_list = []
    other_users_open_tasks_list = []
    failed_tasks_list = []
    user_closed_tasks_list = []

    for task in open_tasks_list_by_urgancy_list:  
        if can_user_acess_discussion(task.parent, request.user):      
            if task.responsible == user:
                user_s_open_tasks_list.append(task)
            else:
                discussion = task.parent
                if user in discussion.get_followers_list():
                    other_users_open_tasks_list.append(task)
                
    tasks_by_recent_closed_at_date = Task.objects.all().exclude(status = Task.MISSED).order_by("-closed_at")

    for task in tasks_by_recent_closed_at_date:
        discussion = task.parent
        if user in discussion.get_followers_list() and can_user_acess_discussion(discussion, request.user):
            status = task_get_status(task)
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
        if user in discussion.get_followers_list() and can_user_acess_discussion( discussion, request.user):
            user_discussions_active.append(discussion)

    for discussion in locked_discussions_by_relevancy_list:
        if user in discussion.get_followers_list() and can_user_acess_discussion( discussion, request.user):
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
            
    return render(request, 'coplay/coplay_report.html',
                  {
                      'number_of_closed_tasks'           : number_of_closed_tasks,
                      'number_of_closed_tasks_for_others': number_of_closed_tasks_for_others,
                      'number_of_aborted_tasks'          : number_of_aborted_tasks,
                      'number_of_task_closing'           : number_of_task_closing,
                      'number_of_views'                  : number_of_views       ,
                      'number_of_feedbacks'              : number_of_feedbacks   ,
                      'number_of_votes'                  : number_of_votes       ,
                      'user_updates_that_viewer_can_access_list': user_updates_query_set,
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
                      'location_desc': user.userprofile.location_desc,
                      'followed_discussions_tags': user.userprofile.followed_discussions_tags.all() } )

class UpdateDiscussionDescForm(forms.ModelForm):
    
    class Meta:
        model = Discussion
        fields = (
            'title',
            'description',
            'location_desc',
            'tags',
            'parent_url',
            'parent_url_text',
            'picture'
        )
        
        widgets = {
            'title': forms.Textarea( attrs={'rows': 1 ,'cols' : 40}),
            'description': forms.Textarea( attrs={'rows': 10 ,'cols' : 40}),
            'location_desc': forms.Textarea(attrs={'rows': 1 ,'cols' : 40}),
            'tags': TagWidgetBig(attrs={'rows': 3 ,'cols' : 40}),
            'parent_url': forms.Textarea(attrs={'rows': 1 ,'cols' : 40}),
            'parent_url_text': forms.Textarea(attrs={'rows': 1 ,'cols' : 40}),
            'picture': forms.ClearableFileInput ,
        }
        
        

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

#         resp = super(UpdateDiscussionDescView, self).form_valid(form)  
        
        tags_string = ''
        found = False
        for name in form.instance.tags.names():
            if found:
                tags_string += ','
            tags_string += name
            found = True
        
        discussion, error_string = discussion_update(  form.instance, 
                                                       self.request.user, 
                                                       form.instance.description, 
                                                       tags_string = tags_string, 
                                                       location_desc = form.instance.location_desc, 
                                                       parent_url = form.instance.parent_url,
                                                       parent_url_text = form.instance.parent_url_text,
                                                       picture         = form.instance.picture)
        
        if discussion:
            return HttpResponseRedirect(discussion.get_absolute_url()) # Redirect after POST

        
        return render(self.request, 'coplay/message.html',
                              {'message': error_string,
                               'rtl': 'dir="rtl"'})


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
        task, error_string = discussion_add_task(self.discussion, 
                                                 self.request.user, 
                                                 form.instance.goal_description, 
                                                 form.instance.target_date)        
        if task:
            return HttpResponseRedirect(
                    task.get_absolute_url())

        return render(self.request, 'coplay/error.html',
                              {'message': error_string,
                               'url': self.discussion.get_absolute_url(),
                               'url_text': u"בחזרה ל" + self.discussion.title,
                               'rtl': 'dir="rtl"'})


class CreateFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            'feedbabk_type',
            'content',
            'voice_recording',
        )
        widgets = {
            'content': forms.Textarea,
            'feedbabk_type': forms.Select,
            'voice_recording': forms.FileInput,
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
#         if Feedback.objects.filter( discussion = self.discussion, feedbabk_type = form.instance.feedbabk_type, content = form.instance.content).exists():
#             return HttpResponseRedirect(
#                     self.discussion.get_absolute_url())
            
#         resp = super(CreateFeedbackView, self).form_valid(form) 
         
        feedback, error_string = discussion_add_feedback( discussion    = self.discussion, 
                                                         user           = self.request.user   ,
                                                         feedbabk_type  = form.instance.feedbabk_type, 
                                                         content        = form.instance.content,
                                                         voice_recording = form.instance.voice_recording)
        if feedback:
            return HttpResponseRedirect(form.instance.discussion.get_absolute_url()) # Redirect after POST
        
        return render(self.request, 'coplay/error.html',
                              {'message': error_string,
                               'url': self.discussion.get_absolute_url(),
                               'url_text': u"בחזרה ל" + self.discussion.title,
                               'rtl': 'dir="rtl"'})
        
#         return resp


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
        
        self.discussion = get_object_or_404(Discussion, id=self.kwargs['pk'])
        if self.discussion.owner != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(CreateDecisionView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        
        decision, error_string = discussion_add_decision(self.discussion, 
                                                         self.request.user,
                                                         form.instance.content)

        if decision:
            return HttpResponseRedirect(self.discussion.get_absolute_url()) # Redirect after POST
        
        return render(self.request, 'coplay/error.html',
                              {'message': error_string,
                               'url': self.discussion.get_absolute_url(),
                               'url_text': u"בחזרה ל" + self.discussion.title,
                               'rtl': 'dir="rtl"'})

            

@login_required
def start_follow_user(request, username):
    try:
        following_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'לא נמצא',
                       'rtl': 'dir="rtl"'})
    
    
    if not is_in_the_same_segment(request.user, following_user):
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


@login_required
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
        

def discussion_tag_list(request, pk = None):
    followers = []
    
    if pk:
        try:
            tag = Tag.objects.get(id=int(pk))
        except Tag.DoesNotExist:
            return render(request, 'coplay/message.html',
                          {'message': 'הנושא איננו קיים',
                           'rtl': 'dir="rtl"'})
        page_name = u'רשימת פעילויות בנושא: ' + tag.name
        
        for user in User.objects.all():
            if tag.name in user.userprofile.followed_discussions_tags.names():
                followers.append(user)
    else:
        page_name = u'מי צריך עזרה?'
        tag = None
    

    tags_set = set ()
    active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()
    
    all_discussions_list  = active_discussions_by_urgancy_list + locked_discussions_by_relevancy_list
    allowed_all_discussions_list = []
    for discussion in all_discussions_list:
        if can_user_acess_discussion(discussion, request.user):
            for tag_iter in discussion.tags.all():
                tags_set.add(tag_iter)
            if tag:
                if tag in discussion.tags.all():
                    allowed_all_discussions_list.append(discussion)
            else:
                allowed_all_discussions_list.append(discussion)
               
    is_following = False
    if request.user.is_authenticated() and tag and tag in request.user.userprofile.followed_discussions_tags.all():
        is_following = True           
        
    
    return render(request, 'coplay/discussion_list.html',
                  {'latest_discussion_list': allowed_all_discussions_list,
                   'tag': tag,
                   'page_name': page_name,
                   'tags_list': tags_set,
                   'tag': tag,
                   'is_following': is_following,
                   'followers': followers})


def discussion_url_list(request):
#     return     'hughu'
#     pprint( request)
    search_url = request.REQUEST.get('search_url', '')
    return render(request, 'coplay/message.html',
                      {'message': search_url,
                       'rtl': 'dir="rtl"'})
    
#     pprint( request)
    
    sys.exit()
    if search_url:
        active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()
         
        all_discussions_list  = active_discussions_by_urgancy_list + locked_discussions_by_relevancy_list
        list_title_min_length = 10000
        list_title = None
        applicabale_discussions_list = []
        for discussion in all_discussions_list:
            if can_user_acess_discussion(discussion, request.user):
                if search_url in discussion.parent_url:
                    applicabale_discussions_list.append(discussion)
                    if len(discussion.parent_url) < list_title_min_length:
                        list_title_min_length = len(discussion.parent_url)
                        list_title = discussion.parent_url_text
        if list_title:
            page_name = u'פעילויות שקשורות ל' + list_title
        else:
            page_name = u'פעילויות שקשורות ל' + search_url
             
                         
        return render(request, 'coplay/discussion_url_list.html',
                      {'applicabale_discussions_list': applicabale_discussions_list,
                       'list_title': page_name,
                       'page_name': page_name})
             
    return HttpResponseRedirect(reverse('coplay:discussions_list'))



@login_required
def start_follow_tag( request, pk):
    try:
        tag = Tag.objects.get(id=int(pk))
    except Tag.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'הנושא איננו קיים',
                       'rtl': 'dir="rtl"'})
                
    start_tag_following( request.user, tag)
            
    return HttpResponseRedirect(reverse('coplay:discussion_tag_list', kwargs={'pk': tag.id}))

def related_discussions_of_url(request):
    search_url = request.REQUEST.get('search_url', '')
    applicabale_discussions_list, list_title = get_discussion_with_parent_url_list( search_url, request.user)
    if list_title:
        page_name = u'פעילויות שקשורות ל' + list_title
    else:
        page_name = u'פעילויות שקשורות ל' + search_url
               
#     return render(request, 'coplay/discussion_list.html',
#                   {'latest_discussion_list': applicabale_discussions_list,
#                    'page_name': page_name})
                           
    return render(request, 'coplay/discussion_url_list.html',
                  {'applicabale_discussions_list': applicabale_discussions_list,
                   'list_title': page_name,
                   'page_name': page_name})

def add_on_discussion_url_list(request):
    search_url = request.REQUEST.get('search_url', '')
    if search_url:
        active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()
         
        all_discussions_list  = active_discussions_by_urgancy_list + locked_discussions_by_relevancy_list
        list_title_min_length = 10000
        list_title = None
        applicabale_discussions_list = []
        for discussion in all_discussions_list:
            if can_user_acess_discussion(discussion, request.user):
                if search_url in discussion.parent_url:
                    applicabale_discussions_list.append(discussion)
                    if len(discussion.parent_url) < list_title_min_length:
                        list_title_min_length = len(discussion.parent_url)
                        list_title = discussion.parent_url_text
        if list_title:
            page_name = u'פעילויות שקשורות ל' + list_title
        else:
            page_name = u'פעילויות שקשורות ל' + search_url
             
                         
        return render(request, 'coplay/discussion_url_list.html',
                      {'applicabale_discussions_list': applicabale_discussions_list,
                       'list_title': page_name,
                       'page_name': page_name})
             
    return HttpResponseRedirect(reverse('coplay:discussions_list'))


    
@login_required
def stop_follow_tag( request, pk):
    try:
        tag = Tag.objects.get(id=int(pk))
    except Tag.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'הנושא איננו קיים',
                       'rtl': 'dir="rtl"'})
        
    stop_tag_following( request.user, tag )

    return HttpResponseRedirect(reverse('coplay:discussion_tag_list', kwargs={'pk': tag.id}))

    
    
