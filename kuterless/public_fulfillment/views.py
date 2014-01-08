# -*- coding: utf-8 -*->
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
    })

    return HttpResponse( 'home' )
    


def labs_root(request):
    
    text_block_0 = """
ועכשיו -  גרסה מיוחדת של האתר שגם תעזור לכולם לתרגל את האנגלית.
ומה עוד?
כמו סגרדה פמיליה בברצלונה, הבניה של האתר אף פעם לא תסתיים.
אז כרגע הגיעו לעבודה באתר שלשה פועלים ומיישרים את השטח לפני שיגיע האיש של הקידוחים.
ו.... בחפירה הראשונה כבר נתקלנו באוצר. 
פיתחנו גירסה אינטרנטית למשחק שעוזר לכל אחד לקדם כל יוזמה או לפתור כל בעיה בעזרתה של קבוצה. 
אז אנחנו מחברים את הסקופ, קולבות,פרובים, לוג'יק אנלייזר, מבחנות, קונדסטורים, (פה אפשר להוסיף כל מיני מילים מפוצצות ומיסתוריות ). מחברים גם צב"ד עוגיות. ולמה? כי אנחנו מתים מסקרנות לדעת אם ואיך כל אחד יעזר בכלי וכדי למדוד איך להמשיך בכיוון הכי נכון. 
אז בכניסתך למעבדה דע/י שכל הפעילות נמדדת ונרשמת !
אף אחד לא יודע איך זה יתפתח. אבל ככה (אנחנו מאמינים) כולנו ביחד נמשיך לבנות ולבנות ולבנות....

והיום, חם מהתנור
מערכת CoPlayWeb

"""
    return render(request, 'public_fulfillment/labs_root.html', {
        'text_block_0': text_block_0,
    })



class CreateUserView(CreateView):
    model = User
    template_name = 'public_fulfillment/user_form.html'
    

def sign_up(request):
    return HttpResponse('sign_up')
