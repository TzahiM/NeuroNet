# -*- coding: utf-8 -*->
from classytags import models
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView

# Create your views here.


def about(request):
    text_block_0 = ''
    return render(request, 'public_fulfillment/public_fulfillment_root.html', {
        'text_block_0': text_block_0,
        'rtl': 'dir="rtl"'
    })

    
    


def labs_root(request):
    
    text_block_0 = """
כמו סגרדה פמיליה בברצלונה, הבניה של האתר אף פעם לא תסתיים.
אז כרגע הגיעו לעבודה באתר שלשה פועלים ומיישרים את השטח לפני שיגיע האיש של הקידוחים.
ו.... בחפירה הראשונה כבר נתקלנו באוצר. 
פיתחנו גירסה אינטרנטית למשחק שעוזר לכל אחד לקדם כל יוזמה או לפתור כל בעיה בעזרתה של קבוצה. 
אז אנחנו מחברים את הסקופ, קולבות,פרובים, לוג'יק אנלייזר, מבחנות, קונדסטורים, (פה אפשר להוסיף כל מיני מילים מפוצצות ומיסתוריות ). מחברים גם צב"ד עוגיות. ולמה? כי אנחנו מתים מסקרנות לדעת אם ואיך כל אחד יעזר בכלי וכדי למדוד איך להמשיך בכיוון הכי נכון. 
אז בכניסתך למעבדה דע/י שכל הפעילות נמדדת ונרשמת !
אף אחד לא יודע איך זה יתפתח. אבל ככה (אנחנו מאמינים) כולנו ביחד נמשיך לבנות ולבנות ולבנות....

"""
    return render(request, 'public_fulfillment/labs_root.html', {
        'text_block_0': text_block_0,
        'rtl': 'dir="rtl"'
    })



class CreateUserView(CreateView):
    model = User
    template_name = 'public_fulfillment/user_form.html'
    

class AddTUserForm(forms.Form):
    user_name  = forms.CharField( max_length = 200)
    password1  = forms.CharField( widget=forms.PasswordInput)
    password2  = forms.CharField( widget=forms.PasswordInput)
    first_name = forms.CharField(  required = False, max_length = 200)
    last_name  = forms.CharField( required = False, max_length = 200)
    email      = forms.EmailField( required = False)      


def sign_up(request):
    if request.user.is_authenticated():
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'Already logged in',
                       'rtl': 'dir="rtl"'})

    if request.method == 'POST': # If the form has been submitted...
        form = AddTUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                return render(request, 'coplay/message.html', 
                      {  'message'      :  'אין התאמה בין שתי הסיסמאות',
                       'rtl': 'dir="rtl"'})
                
            user_name =  form.cleaned_data['user_name']
            
            if User.objects.filter( username = user_name ).exists():
                return render(request, 'coplay/message.html', 
                      {  'message'      :  'משתמש %s קיים.' % (user_name),
                       'rtl': 'dir="rtl"'})
                
            first_name = form.cleaned_data['first_name']
            last_name =  form.cleaned_data['last_name']
            email     =  form.cleaned_data['email']
            user = User(
                    username=user_name,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )

            user.set_password(password1)
            user.save()    
            user = authenticate(username=user_name, password=password1)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                    # Redirect to a success page.
                else:
                    # Return a 'disabled account' error message
                    return render(request, 'coplay/message.html', 
                      {  'message'      :  'disabled account',
                       'rtl': 'dir="rtl"'})
            else:
                # Return an 'invalid login' error message.
                return render(request, 'coplay/message.html', 
                      {  'message'      :  'invalid login account',
                       'rtl': 'dir="rtl"'})
        else:
            return render(request, 'coplay/message.html', 
                      {  'message'      :  'הנתונים אינם מלאים',
                       'rtl': 'dir="rtl"'})
            
        
    else:
        form = AddTUserForm() # An unbound form


    return render(request, 'public_fulfillment/new_user.html', {
        'form': form,
        'rtl': 'dir="rtl"'
    })
    
