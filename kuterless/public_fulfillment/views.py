from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.views.generic.edit import CreateView

# Create your views here.


def home(request):
    return HttpResponse('hi')


def labs_root(request):
    return HttpResponse('labs main')


class CreateUserView(CreateView):
    model = User

def sign_up(request):
    return HttpResponse('sign_up')
