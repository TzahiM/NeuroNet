# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import unicodedata
from django.template.loader import render_to_string
from django.template.base import Template
from django.template.context import Context
from coplay.control import string_to_email_subject
from coplay.control import send_html_message
from NeuroNet import settings



#logger = logging.getLogger(__name__)


def func_name():
    return traceback.extract_stack(None, 2)[0][2]
    
def split_file_name_and_file_extention(filename):
   loc_of_dot = filename.find('.')
   name = filename[:loc_of_dot]
   extention = filename[loc_of_dot:]
   return name,extention
   
#http://source.mihelac.org/search/?q=ant
class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)


def simple_auth_token( key):
    if key is None:
        return None
    
    for user in User.objects.all():
        if user.auth_token.key == key:
            return user        
    return None
        
    
def send_email_message_to_user(user, subject, message):
    email_template = "email_message_to_user.html"
    lang_direction = "rtl"

    if settings.LANGUAGE_CODE is 'he':
        lang_direction = 'ltr'
        email_template =  "email_message_to_user_hebrew.html"
    
    html_message = render_to_string(email_template,
                                    {'ROOT_URL': settings.SITE_URL,
                                     'page_lang': settings.LANGUAGE_CODE,
                                     'lang_direction': lang_direction,
                                     'username': user.username,
                                     'first_name': user.first_name,
                                     'html_title': string_to_email_subject(subject),
                                     'details': message})
    

#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_message)
    
    if user.email != None and user.userprofile.recieve_updates:
        send_html_message(subject, html_message,
                              settings.DEFAULT_FROM_EMAIL,
                              [user.email])






def send_any_email_message_to_user(user, subject = '', template = '', parameters_dict={}):
    
    message = Template(template).render(Context(parameters_dict))

    send_email_message_to_user(user,subject, message)
