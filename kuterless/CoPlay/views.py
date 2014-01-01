from coplay import models
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

# Create your views here.
def root(request):
    return render(request, 'coplay/co_play_root.html')
    

class IndexView(generic.ListView):
    model = Discussion
    template_name = 'coplay/discussion_list.html'
    context_object_name = 'latest_discussion_list'
    

    def get_queryset(self):
        return Discussion.objects.order_by('-updated_at')
    
class AddFeedbackForm(forms.Form):
    feedbabk_type = forms.ChoiceField( choices=Feedback.FEEDBACK_TYPES)
    content = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '80', 'rows': '5'}))

class UpdateDiscussionForm(forms.Form):
    description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '80', 'rows': '5'}))
 
    
class AddDecisionForm(forms.Form):
    content = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '80', 'rows': '5'}))


class VoteForm(forms.Form):
    value = forms.ChoiceField(widget = forms.RadioSelect,  choices=LikeLevel.level)


class AddTaskForm(forms.Form):
    goal_description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '80', 'rows': '5'}))
    target_date =  forms.DateTimeField(widget=SelectDateWidget)

class UpdateTaskForm(forms.Form):
    status_description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea(attrs= {'cols': '80', 'rows': '5'}))


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
    
     
    feedback_form =AddFeedbackForm()
    description_form = UpdateDiscussionForm()
    add_decision_form = AddDecisionForm()
    
    request_user = User.objects.first()
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
            'request_user'    : request_user    ,
            'vote_form'       : vote_form       ,
            'add_task_form'   : add_task_form   })




class NewDiscussionForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(max_length=models.MAX_TEXT, widget=forms.Textarea)
    

def add_discussion(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = User.objects.first()
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
    
    


    
    
def add_feedback(request, pk):   
    if request.method == 'POST': # If the form has been submitted...
        form = AddFeedbackForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = User.objects.first()
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            discussion.add_feedback( user,  form.cleaned_data['feedbabk_type'] , form.cleaned_data['content'])
    return HttpResponseRedirect(discussion.get_absolute_url()) # Redirect after POST
    
def add_decision(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddDecisionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            discussion.add_decision( form.cleaned_data['content'] )
    return HttpResponseRedirect(discussion.get_absolute_url()) # Redirect after POST
        
    
def vote(request, pk):    
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                decision = Decision.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Decision not found')
            user = User.objects.first()
            decision.vote( user, int(form.cleaned_data['value']) )
            try:
                discussion = Discussion.objects.get(id=decision.parent_id)
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            return HttpResponseRedirect( discussion.get_absolute_url()) # Redirect after POST
        return( HttpResponse('Invalid form'))        
        
    return( HttpResponse('Forbidden request not via form'))        
            
            
            

def add_task(request, pk):    
    if request.method == 'POST': # If the form has been submitted...
        form = AddTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = User.objects.first()
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            target_date = form.cleaned_data['target_date']
            if target_date <=  timezone.now():
                response_string= """<p>target date should be in the future<\p>
                <a href=""" + discussion.get_absolute_url() +'">Back To Discussion</a>'
                return HttpResponse(response_string)
            new_task = discussion.add_task( user,  
                                 form.cleaned_data['goal_description'] ,
                                 form.cleaned_data['target_date'] )
            return HttpResponseRedirect(new_task.get_absolute_url()) # Redirect after POST

    return HttpResponseRedirect(reverse ('coplay_root')) # Redirect after POST

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
        
        
    update_task_form = UpdateTaskForm()    
    
    allowed_to_close = True
        
        
        
        
        
    return render(request, 'coplay/task_detail.html', 
                      {  'task'  :  task ,
                       'update_task_form' : update_task_form,
                       'allowed_to_close' : allowed_to_close})
    
    
    
    
    
def update_task_description(request, pk):  
    if request.method == 'POST': # If the form has been submitted...
        form = UpdateTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                task = Task.objects.get(id=int(pk))
            except Task.DoesNotExist:
                return HttpResponse('Task not found')
            task.update_status_description( form.cleaned_data['status_description'] )
            return HttpResponseRedirect(task.get_absolute_url()) # Redirect after POST
        
    error_message = 'Posible only by form'
    resirect_links = []
    resirect_links.append(Link(url = reverse('coplay_root'), text = 'Home'))
    return render(request, 'coplay/error.html', 
                      {  'links'      :  resirect_links,
                         'error_message':error_message})
        
   
def close_task(request, pk):      
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    user = User.objects.all()[1]
    if task.close( user ):
        return HttpResponseRedirect(task.get_absolute_url()) # Redirect after POST
    error_message = 'Cannot close this task'
    resirect_links = []
    resirect_links.append(Link(url = reverse('coplay_root'), text = 'Home'))
    resirect_links.append(Link(url =task.get_absolute_url(), text = 'Baky to tsak details'))
    return render(request, 'coplay/error.html', 
                      {  'links'      :  resirect_links,
                         'error_message':error_message})


