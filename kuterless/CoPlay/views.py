from coplay.models import Discussion
from django.views import generic
from django.views.generic.edit import CreateView

# Create your views here.
def root(request):
    

class IndexView(generic.ListView):
    template_name = 'coplay/index.html'
    context_object_name = 'latest_discussion_list'


class DetailView(generic.DetailView):
    model = Discussion
    template_name = 'coplay/discussion_details.html'


class DiscussionAddView(CreateView):
    model = Discussion

def update_discussion(request, pk):
    
    
def add_decision(request, pk):    
    
def vote(request, pk):    

def add_task(request, pk):    
    
def task_details(request, pk):    
    
    
def update_task_description(request, pk, new_description):  
    
def close_task(request, pk):      


