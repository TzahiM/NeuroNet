from coplay.models import Discussion
from django.http.response import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView

# Create your views here.
def root(request):
    return HttpResponse("root")
    

class IndexView(generic.ListView):
    model = Discussion
    template_name = 'coplay/index.html'
    context_object_name = 'latest_discussion_list'


class DetailView(generic.DetailView):
    model = Discussion
    template_name = 'coplay/discussion_details.html'


class DiscussionAddView(CreateView):
    model = Discussion

def update_discussion(request, pk):
    return HttpResponse("update_discussion" + pk)
    
    
def add_decision(request, pk):
    return HttpResponse("add_decision" + pk)
        
    
def vote(request, pk):    
    return HttpResponse("vote" + pk)

def add_task(request, pk):    
    return HttpResponse("add_task" + pk)
    
def task_details(request, pk):    
    return HttpResponse("task_details"  + pk)
    
    
def update_task_description(request, pk, new_description):  
    return HttpResponse("update_task_description " + new_description)
   
def close_task(request, pk):      
    return HttpResponse("close_task" + pk)


