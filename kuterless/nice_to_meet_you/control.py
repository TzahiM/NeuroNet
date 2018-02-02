# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework.authtoken.models import Token
from taggit.models import Tag
import kuterless.settings
#from gtts import gTTS
import pyqrcode
from kuterless.settings import SITE_URL, MEDIA_URL

def get_sound_to_play_name(acquaintance_id):
#    return "media/message" + str(acquaintance_id)+".mp3"
    num_of_messages = 8
    return "audio_messages/default_message"+str(acquaintance_id % num_of_messages)+".mp3"
    
def get_buisness_card_name(buisness_card_id):
    return "media/buisness_card" + str(buisness_card_id)+".vcf"

def get_buisness_qr_code_image_name(buisness_card_id):
    return MEDIA_URL + "buisness_card_qr" + str(buisness_card_id)+".png"

def update_vcf_file(buisness_card_id,private_name = '',family_name = '', email = '', phone_number = '', url = ''):
    serialized_vcard = ''
    serialized_vcard += 'BEGIN:VCARD\r\n'#BEGIN:VCARD
    serialized_vcard += 'VERSION:3.0\r\n'#VERSION:3.0
    serialized_vcard += 'FN:'+ private_name + ' '  + family_name + '\r\n'#FN:Pname Fname
    serialized_vcard += 'N:'+ family_name + ';' + private_name + ';;;\r\n'#N:Fname;Pname;;;
    serialized_vcard += 'EMAIL;TYPE=INTERNET;TYPE=HOME:' + email + '\r\n'#EMAIL;TYPE=INTERNET;TYPE=HOME:mail@home.com
    serialized_vcard += 'TEL;TYPE=CELL:' + phone_number + '\r\n'#TEL;TYPE=CELL:0522947775
    if url:
        serialized_vcard += 'URL:'+ url + '\r\n'#URL:hp.com
    serialized_vcard += 'END:VCARD\r\n'#END:VCARD
    with open(get_buisness_card_name(buisness_card_id), "wb") as f:
        f.write( serialized_vcard)
        
        
    buisness_card_url = reverse('nice_to_meet_you:scan_card', kwargs={'pk': str(buisness_card_id)})

    url = pyqrcode.create(SITE_URL + buisness_card_url)
    with open(get_buisness_qr_code_image_name(buisness_card_id)[1:], 'wb') as fstream:
        url.png(fstream, scale=5)
        
        
    
    
def update_sound_to_play_file(acquaintance_id, message):

    return None
#    tts_object = gTTS( text = message, lang='en', slow=False)
    
#    tts_object.save(get_sound_to_play_name(acquaintance_id))



