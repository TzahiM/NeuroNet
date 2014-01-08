# -*- coding: utf-8 -*->
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView

# Create your views here.


def home(request):
    return HttpResponse( 'home' )
    


def labs_root(request):
    
    text_block_0 = """
תמיד בבניה !
---------
מה יש?
"""
    return render(request, 'public_fulfillment/labs_root.html', {
        'text_block_0': text_block_0,
    })

    
    '| linebreaks'
    return HttpResponse('labs main')


class CreateUserView(CreateView):
    model = User
    template_name = 'public_fulfillment/user_form.html'
    

def sign_up(request):
    return HttpResponse('sign_up')
