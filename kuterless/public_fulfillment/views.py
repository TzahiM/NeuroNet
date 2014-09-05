# -*- coding: utf-8 -*-
from coplay.control import init_user_profile
from coplay.models import UserProfile
from coplay.views import user_coplay_report
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.utils.http import is_safe_url
from django.views.generic.edit import CreateView
from kuterless import settings
from memecache.control import init_user_account
from django.utils.translation import ugettext as _

# Create your views here.


def about(request):
    text_block_0 = ''
    return render(request, 'public_fulfillment/public_fulfillment_root.html', {
        'text_block_0': text_block_0,
        'rtl': 'dir="rtl"'
    })

def root(request):
    if request.user.is_authenticated():
        if request.user.userprofile.a_player:
            return HttpResponseRedirect(reverse('memecache:root'))            
        return HttpResponseRedirect(reverse('coplay:user_coplay_report', kwargs={'username': request.user.username}))
    
    return about(request)
    
    


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
6/9/2014:
מימוש API לכל אובייקטי coplay
26/8/2014:
תיקון בעיה בעדכון מצב קבלת מיילים
23/8/2014:
תיקון בעיה בתיעוד צפיות אנונימיות
תיקון הכנסה כפולה של משימות ותגובות ורעיונות
22/8/2014:
הוספת יכולת לבטל את שליחת המיילים
רישום כל התעדכנות בכל עילות של משתמשים
תיעוד צפיות אנונימיות של משתמשים  - ראה בכל פעילות את חלק הצפיות האנונימיות
שיוך צפיה של משתמש בהיותו אנונימי למשתמש
הוספת מודל תגמול הכולל חנות פרסים ומימושם

9/7/2014:
ניקודי הצפיה יתאפשרו רק אם באמת היו שינויים בפעילות
8/7/2014:
בעמוד המשתמש, כל הפניה מעדכון, עוברת ישירות לקישור המבוקש
בעוד שהודעות ארוכות עוברות דרך פירוט של התוכן.
נוסף גם הבלטה של עדכונים שעוד לא נקראו על ידי המקבל
7/7/2014:
העידכונים שנשלחו במייל מופיעים עכשיו גם בעמוד הבית של כל משתמש
הוספת אפשרות למנהל פעילות להציג את הקישור שיוכל לשתף. מי שיקבל את הקישור יתבקש להירשם לשם קבלת עדכונים
4/7/2014:
גרסת api מינימלית לדיבוג
1/7/2014:
הוספת יכולת למדר קבוצה של משתמשים - למטרות מחקר
12/6/2014:
קבלת הודעה על התחלת עקיבה והזמנה לעקיבה בחזרה
11/6/2014:
הוספת יכולת להתחיל הרשמה של כל משתמש  בתור עוזר/ת של כל משתמש אחר או  להפסיק את הרישום הזה לאותו  המשתמש.
כשכל משתמש יותר פעילות חדשה אז כל העוזרים הרשומים שלו שלו יקבלו הודעה על בקשת עזרה במייל.
הפעלת והפסקת הקבלה של בקשות העזרה  מופיעות בתור פקד כתום או תכלת בסמוך לשם  המשתמש  שבעמוד שלו.
בתחתית  העמוד של כל משתמש מופיעה רשימת העוזרים הרשומים שלו וגם את רשימת המשתמשים  שהוא משתמש רשום שלהם.
הוספה בכל דף פעילות גם את רשימת מקבלי העדכונים
9/6/2014:
הוספת יכולת לכל משתמש להתחיל לקבל עידכונים במייל או להפסיק  לקבל עידכונים.
זה מופיע בתור פקד כתום או תכלת בסמוך לשם מוביל הפעילות שבתיאור הפעילות 
25/5/2014:
שינוי השם "התלבטויות" להיות "רעיונות להצבעה"
21/5/2014:
הוספת מונה עבור מספר הפעמים שכל משתמש הצביע על התלבטויות בפעילויות של אחרים
תיקון באגים שגרמו להודעות שגיאה בכל עדכון/יצירה של פעילויות ומשימות
התראות והודעות במייל מנוסחות בפירוט של מה קרה ומה צריך לעשות
20/5/2014:
תיקון בעיות בעידכונים של פעילויות
19/5/2014:
הוספת אפשרות לפתיחה מחדש של משימה
שינויים בדף המשימה
תיקון בעיה של שליחת התראות אודות עדכון יעדים בפעילות
פירוט המידע שמתקבל בהתראות למייל
13/4/2014:
תיקון מונה של מספר משימות שבוטלו בזמן
11/4/2014:
הוספת אפשרות לבטל משימה בזמן
2/4/2014:
הוספת מונה עבור סגירת משימות
1/4/2014:
הוספת מדדי צפיה ופעילות של המשתמשים
23/3/2014:
הפיכת קישורים לאתרים אחרים להיפתח בחלונות אחרים או טאבים של הדפדפן
9/3/2014:
חזרה לאותו עמוד אחרי הרשמה(issue #6)
5/3/2014:
טיוב העיצוב של דפי הפעילויות
הפרדת עדכוני מטרות הפעילות ויצירת משימה והוספת ההתלבטויות לטפסים נפרדים 
תיקון אי בדיקת האורך בטפסים(issue #7)
הוספת קישורים להמשך בכל דפי קרוסלת הפתיחה (issue #5)
25/2/2014:
הרחבת עמודי הפעילות של המשתמשים
תיקון בעיה בקישורים של הודעות המייל
17/2/2014:
ביטול השליחה של מיילים אודות עדכונים למשתמש שביצע אותם.
הוספת עמודי פעילות למשתמשים(issue # 17)
3/2/2014:
הוספה של שליחת מיילים על כל עדכון בפעילות ומשימות הקשורות אליה.
במיילים מופיע הקישור לאתר כדי לצפות בפעילות או המשימה המעודכנת    
29/1/2014:
תיקון בעיה של נעילה מופרזת של פעילויות (issue # 20)
27/1/2014:
תיקון בעיה בהרשמה    
23/1/2014:
עכשיו טפסי ההרשמה נראים נהדר - תודה מיכאל !
הוספת פרפראות
20/1/2014:
תיקון בעית הרשמה וכניסה
הוספת נעילה של פעילויות בהעדר מחויבות של המשתתפים


16/1/2014:
עדכון פרופיל משתמש לרבות סיסמה
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
    
    user_name = forms.CharField( label='', 
        widget=forms.TextInput(attrs={'placeholder': 'שם משתמש', 'class': 'form-control'}))

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

    recieve_email_updates = forms.BooleanField(label=u'קבלת מיילים מהאתר', required = False, initial = True)
    
    
    
def sign_up(request):
    if request.user.is_authenticated():
        return render(request, 'coplay/message.html', 
                      {  'message'      :  'Already logged in',
                       'rtl': 'dir="rtl"'})
    redirect_to = request.REQUEST.get('next', '')
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST': # If the form has been submitted...
        form = AddUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Ensure the user-originating redirection url is safe.

            
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
            init_user_profile(user)
            init_user_account(user)
            user.userprofile.recieve_updates = form.cleaned_data['recieve_email_updates']
            user.userprofile.save()
            
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

def privacy_policy(request):
    return render(request, 'public_fulfillment/privacy_policy.html', {
        'rtl': 'dir="rtl"'
    })


@login_required
def update_profile(request):
    user = request.user
    redirect_to = request.REQUEST.get('next', '')
    if not is_safe_url(url=redirect_to, host=request.get_host()):
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
                
            user.userprofile.recieve_updates = form.cleaned_data['recieve_email_updates']
            
            user.userprofile.save()
            
            user.save()

        return HttpResponseRedirect(redirect_to) # Redirect after POST
                                
    else:
        form = UpdateProfileUserForm( initial=
                                      {'first_name': user.first_name,
                                       'last_name' : user.last_name,
                                       'email'     : user.email,
                                       'recieve_email_updates': user.userprofile.recieve_updates}
                                      )

    return render(request, 'public_fulfillment/update_user.html', {
        'form': form,
        'next': redirect_to,
        'rtl': 'dir="rtl"'
    })
    

@login_required
def stop_email(request):
    user = request.user
    user.userprofile.recieve_updates = False
    user.userprofile.save()
    user.save()

    return render(request, 'coplay/message.html', 
                      {  'message'      :  'הופסקה קבלת המיילים',
                       'rtl': 'dir="rtl"'})
    

    
    
    
