# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import request
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.base import Template
from django.template.context import Context
from django.template.defaultfilters import pprint
from django.utils import six, timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from kuterless.settings import SITE_URL, MEDIA_URL
from taggit.forms import TagField
from taggit.models import Tag
from taggit.utils import edit_string_for_tags
import floppyforms as forms
import sys
#from gtts import gTTS
from shutil import *
from models import *
from control import get_sound_to_play_name, get_buisness_card_name

@login_required
def view_cards (request):
    return render(request, 'nice_to_meet_you/view_cards.html', 
                      {  'cards_list'   :  BusinessCard.objects.all(),})


def scanned_user (request):
    message = request.REQUEST.get('message', '')
#    tts_object = gTTS( text = message, lang='en', slow=False)
#    tts_object.save("media/latest_message.mp3")

#OK    return HttpResponseRedirect('http://127.0.0.1:8000/media/zzz.mp3')
    return render(request, 'nice_to_meet_you/message.html', 
                      {  'message'      :  message,
                       'rtl': 'dir="rtl"'})


def view_card(request, pk):
    try:
        business_card = BusinessCard.objects.get(id=int(pk))
    except BusinessCard.DoesNotExist:
        return None
    return render(request, 'nice_to_meet_you/view_card.html', 
                      {  'card'   :  business_card,})
                       
def scan_card(request, pk):
    try:
        business_card = BusinessCard.objects.get(id=int(pk))
    except BusinessCard.DoesNotExist:
        return None
    

#    message_to_play_text = 'my name is ' + business_card.private_name + ' ' + business_card.family_name + ' nice to meet you'
    message_to_play_text = 'ding ding ding ' + business_card.private_name + ' ' + business_card.family_name 
    if request.user.is_authenticated():
        message_to_play_text = 'It is very nice to meet you, ' + request.user.get_full_name() + ' my name is ' + business_card.private_name + ' ' + business_card.family_name 

#    message_to_play_text = 'ting'
    new_acquaintance = Acquaintance(business_card = business_card, message =  message_to_play_text)
    new_acquaintance.save()

    
#    return HttpResponseRedirect( '/media/contacts.vcf')
    return HttpResponseRedirect( '/'+ get_buisness_card_name(business_card.id) )

    
def get_message(request):
    copyfile("media/latest_message.mp3", "media/message_to_play.mp3")
    copyfile("media/empty.mp3", "media/latest_message.mp3")

    return HttpResponseRedirect("http://127.0.0.1:8000/media/message_to_play.mp3")
#    return HttpResponseRedirect('http://127.0.0.1:8000/media/latest_message.mp3')
    
def get_latest_message(request):
    if Acquaintance.objects.count() is 0:
        return HttpResponseRedirect( '/media/audio_messages/empty.mp3' )
#        return None
    
    acquaintance = Acquaintance.objects.all().order_by("-updated_at").first()
    if acquaintance.is_played:
        return HttpResponseRedirect( '/media/audio_messages/empty.mp3' )
#        return None
    acquaintance.is_played = True
    acquaintance.save()
    return HttpResponseRedirect( '/'+ get_sound_to_play_name(acquaintance.id) )
#    dst_file_name = 'media/'+ get_sound_to_play_name(acquaintance.id)
#    copyfile( get_sound_to_play_name(acquaintance.id), dst_file_name)
#    return HttpResponseRedirect( '/'+ dst_file_name )
     

def message_board(request):
    return render(request, 'nice_to_meet_you/message_board.html')

    
    
        
