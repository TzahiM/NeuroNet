# -*- coding: utf-8 -*-
from coplay.services import MAX_MESSAGE_INPUT_CHARS
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView
from NeuroNet import settings
from public_fulfillment.services import create_kuterless_user
from coplay.services import start_users_following

# Create your views here.


def about(request):
    return HttpResponseRedirect('/media/content/About Coronavirus Hachathon.html')

    text_block_0 = ''
    return render(request, 'public_fulfillment/root.html', {
        'text_block_0': text_block_0,
        'rtl': 'dir="rtl"',
        'about': '/media/content/About.html',
    })

def corona_hackathon_root(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('coplay:user_coplay_report', kwargs={'username': request.user.username}))
    return render(request, 'public_fulfillment/CoronaVirusHackathonRoot.html', {
        #'text_block_0': text_block_0,
        'rtl': 'dir="rtl"',
    })
    

def agreement(request):


    return render(request, 'public_fulfillment/agreement.html', {
        'next': next,
        'rtl': 'dir="rtl"',
    })



@login_required
def back_from_disclaimer(request):
    next = request.GET.get('next')

    if next:
        return HttpResponseRedirect(next)
    return root(request)


    return render(request, 'public_fulfillment/disclaimer.html', {
        'next': next,
        'rtl': 'dir="rtl"',
    })

@login_required
def disclaimer(request):
    next = request.GET.get('next')
    request.user.userprofile.a_player = True
    request.user.userprofile.save()
    admin_user= request.user.userprofile.segment.shop_set.first().admin_user
    start_users_following( admin_user, request.user)
    start_users_following( request.user, admin_user)


    return render(request, 'public_fulfillment/disclaimer.html', {
        'next': next,
        'rtl': 'dir="rtl"',
    })

def root(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('coplay:user_coplay_report', kwargs={'username': request.user.username}))
    return HttpResponseRedirect(reverse('corona_hackathon_root'))

    




class CreateUserView(CreateView):
    model = User
    template_name = 'public_fulfillment/user_form.html'
    

class AddUserForm(forms.Form):
    
    approved_discaimer = forms.BooleanField(label=_(u"קראתי והסכמתי למדיניות הפרטיות"), required = False,initial = False)
    
    user_name = forms.CharField( label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם משתמש באנגלית בלבד', 'class': 'form-control'}))

    password  = forms.CharField( label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'סיסמא', 'class': 'form-control'}))

    password_confirm  = forms.CharField( label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'אותה סיסמא', 'class': 'form-control'}))
    
    first_name  = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם פרטי', 'class': 'form-control'}))
    
    last_name = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם משפחה', 'class': 'form-control'}))
    
    email = forms.EmailField( required = False, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'אימייל', 'class': 'form-control'}))

    recieve_email_updates = forms.BooleanField(label=_(u"קבלת מיילים"), initial = True)

#     followed_discussions_tags = forms.CharField( label=u'נושאים שיענינו אותך', widget = TagWidgetBig(attrs={'rows': 3 ,'cols' : 40} )  )
    
    description = forms.CharField(label=u'לא חובה:כל דבר שתרצה/י להוסיף לרבות איך ליצור איתך קשר',required = False,
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)
    
    location_desc = forms.CharField(label=u'כתובת - לא חובה',
                                  required = False,
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)




class UpdateProfileUserForm(forms.Form):
    password  = forms.CharField( required = False, label='', 
        widget=forms.PasswordInput(attrs={'placeholder': u'password', 'class': 'form-control'}))

    password_confirm  = forms.CharField( required = False, label='', 
        widget=forms.PasswordInput(attrs={'placeholder': u'repeat password', 'class': 'form-control'}))
    
    first_name  = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': u'first name', 'class': 'form-control'}))
    
    last_name = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': u'last name', 'class': 'form-control'}))
    
    email = forms.EmailField( required = False, label='', 
        widget=forms.TextInput(attrs={'placeholder': u'email', 'class': 'form-control'}))

    recieve_email_updates = forms.BooleanField(label=u'recieving emails', required = False, initial = True)
    
#     followed_discussions_tags = forms.CharField( label=u'נושאים שיענינו אותך', widget = TagWidgetBig(attrs={'rows': 3 ,'cols' : 40} )  )
    
    description = forms.CharField(label=u'contact info/about yourself',required = False,
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)
    
    location_desc = forms.CharField(required = False,label=u'Address',
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)
    
    
def sign_up(request):

    if request.user.is_authenticated:
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'Already logged in',
                       'rtl': 'dir="rtl"'})
    #return HttpResponseRedirect("https://forms.gle/c723wnVe3rWrnkdH9")
    
    redirect_to = request.GET.get('next')
    allowed_hosts = []
    allowed_hosts.append(request.get_host())
    if not is_safe_url(url=redirect_to, allowed_hosts = allowed_hosts):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST': # If the form has been submitted...
        form = AddUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Ensure the user-originating redirection url is safe.
            
            if False is form.cleaned_data['approved_discaimer']:
                return render(request, 'coplay/message.html', 
                      {  'message'      :  'עליך לאשר את מדיניות הפרטיות',
                       'rtl': 'dir="rtl"'})
                

            
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password != password_confirm:
                return render(request, 'coplay/message.html', 
                      {  'message'      :  'Password repeat mismatch',
                       'rtl': 'dir="rtl"'})
                
            user_name =  form.cleaned_data['user_name']
            
                
            first_name = form.cleaned_data['first_name']
            last_name =  form.cleaned_data['last_name']
            email     =  form.cleaned_data['email']

            
            recieve_updates = form.cleaned_data['recieve_email_updates']
            
            description = form.cleaned_data['description']
            
            location_desc = form.cleaned_data['location_desc']
            

            user = create_kuterless_user(  user_name, 
                                           password, 
                                           first_name, 
                                           last_name,  
                                           email, 
                                           recieve_updates, 
                                           description, 
                                           location_desc)
            
            
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to) 
                    # Redirect to a success page.
                else:
                    # Return a 'disabled account' error message
                    return render(request, 'coplay/message.html', 
                      {  'message'      :  'disabled account',
                       'rtl': 'dir="rtl"'})
            else:
                # Return an 'invalid login' error message.
                return render(request, 'coplay/message.html', 
                      {  'message'      :  'הכניסה נכשלה',
                       'rtl': 'dir="rtl"'})
        else:
            return render(request, 'coplay/message.html', 
                      {  'message'      :  'הנתונים אינם מלאים',
                       'rtl': 'dir="rtl"'})
            
        return HttpResponseRedirect(redirect_to) # Redirect after POST
        
    else:
        form = AddUserForm() # An unbound form


    return render(request, 'public_fulfillment/new_user.html', {
        'form': form,
        'next': redirect_to,
        'rtl': 'dir="rtl"'
    })
    

def example(request):
    return render(request, 'public_fulfillment/example.html', {
        'rtl': 'dir="rtl"'
    })



@login_required
def update_profile(request):
    user = request.user
    if not user.userprofile:
        return render(request, 'coplay/message.html', 
                    {  'message'      :  'not a user',
                    'rtl': 'dir="rtl"'})

    redirect_to = request.GET.get('next')
    allowed_hosts = []
    allowed_hosts.append(request.get_host())
    if not is_safe_url(url=redirect_to, allowed_hosts = allowed_hosts):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST': # If the form has been submitted...
        form = UpdateProfileUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            password = form.cleaned_data['password']
           
            
            if password:
                    # Process the data in form.cleaned_data# Process the data in form.cleaned_data
                password_confirm = form.cleaned_data['password_confirm']
                
                if password != password_confirm:
                    return render(request, 'coplay/message.html', 
                              {  'message'      :  'None התאמה בין שתי הסיסמאות',
                               'rtl': 'dir="rtl"'})
                user.set_password(password)
                        
            
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']                  
            email =  form.cleaned_data['email']
                
            user.userprofile.recieve_updates = form.cleaned_data['recieve_email_updates']
            
#             user.userprofile.followed_discussions_tags.set(form.cleaned_data['followed_discussions_tags'])
            
            description = form.cleaned_data['description']
            if description:
                user.userprofile.description = description
                
            location_desc = form.cleaned_data['location_desc']
            if location_desc:
                user.userprofile.location_desc = location_desc
                
            user.userprofile.save()
            
            user.save()

        return HttpResponseRedirect(redirect_to) # Redirect after POST
                                
    else:
        form = UpdateProfileUserForm( initial=
                                      {'first_name': user.first_name,
                                       'last_name' : user.last_name,
                                       'email'     : user.email,
                                       'recieve_email_updates': user.userprofile.recieve_updates,
                                       'description': user.userprofile.description,
                                       'location_desc': user.userprofile.location_desc,
                                       'followed_discussions_tags': user.userprofile.followed_discussions_tags.names}
                                      )

    return render(request, 'public_fulfillment/update_user.html', {
        'form': form,
        'next': redirect_to,
        'rtl': 'dir="rtl"'
    })
    

#@login_required
def stop_email(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        username = request.GET.get('username')
        if username:
            user = User.objects.get(username=username)
        else:
            return render(request, 'coplay/message.html', 
                      {  'message'      :  'unknown user',
                       'rtl': 'dir="rtl"'})

    user.userprofile.recieve_updates = False
    user.userprofile.save()
    user.save()

    return render(request, 'coplay/message.html', 
                      {  'message'      :  user.get_full_name()+' had been removed from our mailing list',
                       'rtl': 'dir="rtl"'})
    

    
    
    
