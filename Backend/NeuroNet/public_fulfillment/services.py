# -*- coding: utf-8 -*-
"""
This file contain the services, used for all views
"""
from coplay.control import init_user_profile, init_user_token
from django.contrib.auth.models import User
from memecache.control import init_user_account
from coplay.models import Segment
from excel import OpenExcel
from memecache.models import Shop
from NeuroNet import settings
from public_fulfillment.control import send_email_message_to_user, send_any_email_message_to_user
from django.template.base import Template
from django.template.context import Context


def get_default_email():
    u = User.objects.all()[0]
    return u.email


def get_default_first_name():
    return 'no_first_name'


def get_default_last_name():
    return 'no_last_name'

def get_default_password():
    return settings.DefaultPassword



def create_kuterless_user(  user_name, password = get_default_password(), first_name = get_default_first_name(), last_name = get_default_last_name(), email = get_default_email(), recieve_updates = True, description= None, location_desc = None, followed_discussions_tags = None, segment = None):
    
                
    if User.objects.filter( username = user_name ).count() != 0:        
        return None
    
    user = User(
            username=user_name,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    user.set_password(password)
    user.save()    
    init_user_profile(user, segment)
    init_user_account(user)
    init_user_token(user)
    user.userprofile.recieve_updates = recieve_updates
    user.userprofile.description = description
    user.userprofile.location_desc = location_desc
    user.userprofile.segment = segment
    user.userprofile.save()
    
    return user



def create_or_update_kuterless_user(  user_name, password = get_default_password(), first_name = get_default_first_name(), last_name = get_default_last_name(), email = get_default_email(), recieve_updates = True, description= None, location_desc = None, followed_discussions_tags = None, segment = None):
    user_set = User.objects.filter( username = user_name )
    if user_set.count() != 0:        
        user=user_set[0]
    else:
        user=create_kuterless_user(user_name=user_name)
    
    user.email=email
    user.first_name=first_name
    user.last_name=last_name
    user.set_password(password)
    user.save()
    user.userprofile.recieve_updates = recieve_updates
    user.userprofile.description = description
    user.userprofile.location_desc = location_desc
    user.userprofile.segment = segment
    user.userprofile.save()
    
    return user

from string import ascii_letters

def get_col_names_dict(excel_object):
    col_index = 0
    col_named_dict={}
    col_names=excel_object.read('1')
    for col_name in col_names:
        col_named_dict[col_name] =ascii_letters[col_index]
        print( col_name, ascii_letters[col_index])
        col_index += 1
    return col_named_dict

def get_tags_set( tags_string):
    #print( 'tags_string',tags_string)
    tags_set = []
    for tagg_to_add in tags_string.split(',').strip():
        tagg_to_add =  tag_string.strip().casefold()
        if tag_to_add is 'legal advisory':
            tag_to_add = 'Law'
        if tag_to_add is 'Biology and pharma':
            tag_to_add = 'Science'
        if tag_to_add is 'Organize a Hackathon':
            tag_to_add = 'Event Planning'
        if tag_to_add is 'Product desigh':
            tag_to_add = 'Design(Any)'
        if tag_to_add is 'Electronics':
            tag_to_add = 'HW/Board design/Real time embedded SW/Mechanics etc'
        if tag_to_add is 'Maker':
            tag_to_add = 'HW/Board design/Real time embedded SW/Mechanics etc'
        if tag_to_add is 'Real Time Embedded':
            tag_to_add = 'HW/Board design/Real time embedded SW/Mechanics etc'
        if tag_to_add is 'Loneliness':
            tag_to_add = 'Well being/Loneliness/relieve the stress etc'

        if "willing to join another one's project" not in tagg_to_add and tag_to_add is not 'Take someone with you' and tag_to_add is not 'Attend a public broadcast (if shall take place)' and tag_to_add is not 'I know how things work':
            tags_set.append(tagg_to_add )
        #print( 'add:','<'+ tag_string.strip().casefold()+'>')
    return tags_set


def delete_all(list):
    for item in list:
        if item.id != None:
            item.delete()

def create_segment( admin_username, password, segment_name):
    segments = Segment.objects.filter( title=segment_name)
    if segments:
        return segments[0]

    segment = Segment(title=segment_name)

    segment.save()
    admin_user = create_kuterless_user( user_name=admin_username, password=password, segment=segment)
    shop = Shop(segment = segment     ,
    admin_user =admin_user,     
    title = segment_name)
    shop.save()
    return segment

def delete_kuterless_user( user):
    if not user or user.id == None:
        return

    if user.userprofile:
        user.userprofile.delete()
    user.delete()

def delete_segment( segment):
    if segment==None or segment.id == None:
        return

    for userprofile in segment.userprofile_set.all():
        delete_kuterless_user(userprofile.user)


    segment.shop = None

    segment.delete()



def delete_segment_non_admin_users( segment):
    if segment==None or segment.id == None:
        return

    for userprofile in segment.userprofile_set.all():
        if userprofile.user != segment.shop_set.all()[0].admin_user:
            delete_kuterless_user(userprofile.user)
        
def print_users(segment_name):
    segment = Segment.objects.get(title=segment_name)
    for u in segment.userprofile_set.all():
        print( u.user.email, u.user.first_name, u.user.last_name, u.user.username)





def send_registration_confirmed_email_message_to_user(user):
    
    t = Template("""
This is Tzahi Manistersky, the organizer of corona virus hackathon.                                                  \n
I'm sending you this main because you had applied to join our community,                                             \n
It took us some time for process your application.                                                                   \n
But considering that filling the form is an evidence for your commitment.                                            \n
                                                                                                                     \n
The important thing is that we need new ideas/projects and cooperation.                                              \n
                                                                                                                     \n
Feel free to be one of the first to connect into our system at  https://www.neuronetlabs.org/CoronaVirusHackathon/    \n
1) Your account info:                                                                                                \n
username: {{username}}                                                                                                        \n
This is a link for reset your password: https://www.neuronetlabs.org/reset-password                                   \n
 Once you're in, I'll be notified for any of your projects (idea/ask for support and help)                           \n
                                                                                                                     \n
2) If you are using chrome, I would highly recommend on installing our chrome extension from store:                  \n
https://chrome.google.com/webstore/detail/corona-virus-hackathon/ggkbcckihealpkiafibifobejlamcfpn                    \n
Feel free to contact me:                                                                                             \n
                                                                                                                     \n
Tzahi Manistersky                                                                                                    \n
+972(52)2947775
 """)
        
    message = t.render(Context({"username": user.username}))

    subject = 'Your application to corona virus hackathon had been approved'

    send_email_message_to_user(user,subject, message)


def send_registration_confirmed_email_message_to_user_fix(user):
    subject = 'Default  password if reset-password fails'

    template = """
This is Tzahi Manistersky, the organizer of corona virus hackathon.                                                  \n
We had encountered a bug in reset password.\n
So if is fails, use password:incorrect                                                                                                                     \n
Feel free to be one of the first to connect into our system at  https://www.neuronetlabs.org/CoronaVirusHackathon/    \n                                                                                               \n
username: {{username}}                                                                                                        \n
password: incorrect                                   \n
                                                                                                                     \n
Tzahi Manistersky                                                                                                    \n
+972(52)2947775
 """
    parameters_dict = {"username": user.username}
    send_any_email_message_to_user(user, 
                                   subject = subject, 
                                   template = template, 
                                   parameters_dict = parameters_dict)








