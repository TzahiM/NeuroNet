# -*- coding: utf-8 -*->
from classytags import models
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
כמו סגרדה פמיליה בברצלונה , הבניה של האתר אף פעם לא תסתיים.
אז כרגע הגיעו לעבודה באתר שלשה פועלים ומיישרים את השטח לפני שיגיע האיש של הקידוחים.
ו.... בחפירה הראשונה כבר נתקלנו באוצר. 
פיתחנו גירסה אינטרנטית למשחק שעוזר לכל אחד לקדם כל יוזמה או לפתור כל בעיה בעזרתה של קבוצה. 
אז אנחנו מחברים את הסקופ, קולבות,פרובים, לוג'יק אנלייזר, מבחנות, קונדסטורים, (פה אפשר להוסיף כל מיני מילים מפוצצות ומיסתוריות ). מחברים גם צב"ד עוגיות. ולמה? כי אנחנו מתים מסקרנות לדעת אם ואיך כל אחד יעזר בכלי וכדי למדוד איך להמשיך בכיוון הכי נכון. 
אז בכניסתך למעבדה דע/י שכל הפעילות נמדדת ונרשמת !
אף אחד לא יודע איך זה יתפתח. אבל ככה (אנחנו מאמינים) כולנו ביחד נמשיך לבנות ולבנות ולבנות....

"""

    version_description = """
23/1/2014:
עכשיו טפסי ההרשמה נראים נהדר - תודה מיכאל !
הוספת פרפראות
20/1/2014:
תיקון בעית הרשמה וכניסה
הוספת נעילה של פעילויות בהעדר מחויבות של המשתתפים


16/1/2014:
ערכון פרופיל משתמש לרבות סיסמה
שינוי שם מהחלטות להתלבטויות
היפוך שמאל ימין בטופס פעילות
"""
    return render(request, 'public_fulfillment/labs_root.html', {
        'text_block_0': text_block_0,
        'rtl': 'dir="rtl"',
        'version_description': version_description
    })



class CreateUserView(CreateView):
    model = User
    template_name = 'public_fulfillment/user_form.html'
    

class AddUserForm(forms.Form):
    user_name = forms.EmailField( label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם משתמש', 'class': 'form-control'}))

    password  = forms.CharField( label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'סיסמא', 'class': 'form-control'}))

    password_confirm  = forms.CharField( label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'אימות סיסמא', 'class': 'form-control'}))
    
    first_name  = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם פרטי', 'class': 'form-control'}))
    
    last_name = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם משפחה', 'class': 'form-control'}))
    
    email = forms.EmailField( required = False, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'אימייל', 'class': 'form-control'}))



class UpdateProfileUserForm(forms.Form):
    password  = forms.CharField( required = False, label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'סיסמא', 'class': 'form-control'}))

    password_confirm  = forms.CharField( required = False, label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'אימות סיסמא', 'class': 'form-control'}))
    
    first_name  = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם פרטי', 'class': 'form-control'}))
    
    last_name = forms.CharField( required = False, max_length = 200, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם משפחה', 'class': 'form-control'}))
    
    email = forms.EmailField( required = False, label='', 
        widget=forms.TextInput(attrs={'placeholder': 'אימייל', 'class': 'form-control'}))


def sign_up(request):
    if request.user.is_authenticated():
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'Already logged in',
                       'rtl': 'dir="rtl"'})

    if request.method == 'POST': # If the form has been submitted...
        form = AddUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password != password_confirm:
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

            user.set_password(password)
            user.save()    
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'coplay/message.html', 
                      {  'message'      :  'ברוכים הבאים',
                       'rtl': 'dir="rtl"'})
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
            
        return HttpResponseRedirect(reverse('coplay:coplay_root')) # Redirect after POST
        
    else:
        form = AddUserForm() # An unbound form


    return render(request, 'public_fulfillment/new_user.html', {
        'form': form,
        'rtl': 'dir="rtl"'
    })
    

def example(request):
    return render(request, 'public_fulfillment/example.html', {
        'rtl': 'dir="rtl"'
    })



@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST': # If the form has been submitted...
        form = UpdateProfileUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            password = form.cleaned_data['password']
           
            
            if password:
                    # Process the data in form.cleaned_data# Process the data in form.cleaned_data
                password_confirm = form.cleaned_data['password_confirm']
                
                if password != password_confirm:
                    return render(request, 'coplay/message.html', 
                              {  'message'      :  'אין התאמה בין שתי הסיסמאות',
                               'rtl': 'dir="rtl"'})
                user.set_password(password)
                        
            
            first_name = form.cleaned_data['first_name']
            
            if first_name:
                user.first_name = first_name
            last_name =  form.cleaned_data['last_name']
            
            if last_name:
                user.last_name = last_name                    
            email =  form.cleaned_data['email']
            
            
            
            if email:
                user.email = email
            user.save()

        return HttpResponseRedirect(reverse('coplay:coplay_root')) # Redirect after POST
                                
    else:
        form = UpdateProfileUserForm() # An unbound form


    return render(request, 'public_fulfillment/update_user.html', {
        'form': form,
        'rtl': 'dir="rtl"'
    })
    
    
