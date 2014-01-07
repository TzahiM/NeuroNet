from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView

# Create your views here.


def home(request):
    return HttpResponseRedirect('labs_root') # Redirect after POST
    


def labs_root(request):
    return HttpResponse('labs main')


class CreateUserView(CreateView):
    model = User
    template_name = 'public_fulfillment/user_form.html'
    

def sign_up(request):
    return HttpResponse('sign_up')
