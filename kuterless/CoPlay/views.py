from coplay import models
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import DateTimeInput, DateInput
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

# Create your views here.
def root(request):
    return render(request, 'coplay/co_play_root.html', {'rtl': 'dir="rtl"'})
    

class IndexView(generic.ListView):
    model = Discussion
    template_name = 'coplay/discussion_list.html'
    context_object_name = 'latest_discussion_list'
    

    def get_queryset(self):
        return Discussion.objects.order_by('-updated_at')
    
   
class AddFeedbackForm(forms.Form):
    content = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '40', 'rows': '3'}))
    feedbabk_type = forms.ChoiceField( choices=Feedback.FEEDBACK_TYPES)


class UpdateDiscussionForm(forms.Form):
    description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '40', 'rows': '3'}))
 
    
class AddDecisionForm(forms.Form):
    content = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '40', 'rows': '3'}))


class VoteForm(forms.Form):
    value = forms.ChoiceField(widget = forms.RadioSelect,  choices=LikeLevel.level)


class AddTaskForm(forms.Form):
    goal_description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '40', 'rows': '3'}))
    target_date =  forms.DateTimeField()
    
class UpdateTaskForm(forms.Form):
    status_description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '40', 'rows': '3'}))


def discussion_details(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return HttpResponseRedirect(reverse('coplay_root'))
    
    list_encourage   =discussion.feedback_set.all().filter( feedbabk_type = Feedback.ENCOURAGE  ).order_by( "-created_at")
    list_cooperation =discussion.feedback_set.all().filter( feedbabk_type = Feedback.COOPERATION).order_by( "-created_at")
    list_intuition   =discussion.feedback_set.all().filter( feedbabk_type = Feedback.INTUITION  ).order_by( "-created_at")
    list_advice      =discussion.feedback_set.all().filter( feedbabk_type = Feedback.ADVICE     ).order_by( "-created_at")
    list_decision   =discussion.decision_set.all().order_by( "-created_at") 
    list_tasks       =discussion.task_set.all().order_by( "-created_at")
    like_levels = LikeLevel.level 
    
    vote_form = None
    feedback_form = None
    description_form = None
    add_decision_form = None
    add_task_form = None
    if request.user.is_authenticated():        
        if request.user ==  discussion.owner:
            description_form = UpdateDiscussionForm()
            add_decision_form = AddDecisionForm()
        else:
            feedback_form =AddFeedbackForm()
            vote_form = VoteForm()
    
        add_task_form = AddTaskForm()
    
    
    return render(request, 'coplay/discussion_detail.html', 
         {  'discussion'      :  discussion     ,      
            'list_encourage'  : list_encourage  ,   
            'list_cooperation': list_cooperation, 
            'list_intuition'  : list_intuition  ,
            'list_advice'     : list_advice     ,
            'list_decision'   : list_decision   ,
            'list_tasks'      : list_tasks      ,
            'feedback_form'   : feedback_form   ,
            'description_form': description_form,
            'add_decision_form': add_decision_form,
            'vote_form'       : vote_form       ,
            'add_task_form'   : add_task_form   ,
            'like_levels'     : like_levels})




class NewDiscussionForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea)
    
@login_required
def add_discussion(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            new_discussion = Discussion(owner =  user ,
                                        title =  form.cleaned_data['title'] ,
                                        description = form.cleaned_data['description'])
            new_discussion.clean()
            new_discussion.save()
            return HttpResponseRedirect(new_discussion.get_absolute_url()) # Redirect after POST
    else:
        form = NewDiscussionForm() # An unbound form


    return render(request, 'coplay/new_discussion.html', {
        'form': form,
    })

    


@login_required
def update_discussion(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = UpdateDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            discussion.update_description( form.cleaned_data['description'] )
    return HttpResponseRedirect(discussion.get_absolute_url()) # Redirect after POST
    
    


    
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
            if user != discussion.owner and form.cleaned_data['feedbabk_type']  and form.cleaned_data['content']:
                discussion.add_feedback( user,  form.cleaned_data['feedbabk_type'] , form.cleaned_data['content'])
            return HttpResponseRedirect(discussion.get_absolute_url()) # Redirect after POST
        return HttpResponse('Invalid form. Please')
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
                discussion.add_decision( form.cleaned_data['content'] )
            else:
                return HttpResponse('Forbidden access')
            return HttpResponseRedirect(discussion.get_absolute_url()) # Redirect after POST
        else:
            return HttpResponse('Invalid form')
    return HttpResponseRedirect('coplay_root') # Redirect after POST
        
@login_required    
def vote(request, pk):    
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                decision = Decision.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Decision not found')
            user = request.user
            if user != decision.parent.owner:
                decision.vote( user, int(form.cleaned_data['value']) )
            return HttpResponseRedirect( decision.parent.get_absolute_url()) # Redirect after POST
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'Please select a vote value'})
                
        
    return( HttpResponse('Forbidden request not via form'))        
            
            
            

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
            if target_date <=  timezone.now():
                return HttpResponse( 'target date should be in the future' + str(target_date))
            new_task = discussion.add_task( user,  
                                 form.cleaned_data['goal_description'] ,
                                 form.cleaned_data['target_date'] )
            return HttpResponseRedirect(new_task.get_absolute_url()) # Redirect after POST

    return HttpResponseRedirect('coplay_root') # Redirect after POST

class Link():
    url = ''
    text = ''
    
   
def task_details(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        error_message = 'Task not found'
        resirect_links = []
        resirect_links.append(Link(url = reverse('coplay_root'), text = 'Home'))
        return render(request, 'coplay/error.html', 
                      {  'links'      :  resirect_links,
                         'error_message':error_message})
        
    close_possible = False
    update_task_form = None   
    
    
    
     
    if request.user.is_authenticated():     
        user = request.user   
        if task.get_status() == task.STARTED:
            if user ==  task.responsible:
                update_task_form = UpdateTaskForm()
            else:
                close_possible = True
             
        
    return render(request, 'coplay/task_detail.html', 
                      {  'task'  :  task ,
                       'update_task_form' : update_task_form,
                       'close_possible'   : close_possible})
    
    
    
    
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
                task.update_status_description( form.cleaned_data['status_description'] )
            
    return HttpResponseRedirect(task.get_absolute_url()) # Redirect after POST
        
        
@login_required   
def close_task(request, pk):      
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    user = request.user
    if user != task.responsible:
        task.close( user )
        
    return HttpResponseRedirect(task.get_absolute_url()) # Redirect after POST
    

