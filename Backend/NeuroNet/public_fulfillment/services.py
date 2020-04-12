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


    
def print_col_names( excel_file_name ):
    excel_object = OpenExcel('HackCoronaRegistrationForm_1.xlsx')
    col_named_dict = get_col_names_dict(excel_object)
    #print( col_named_dict)
    #for row_index in range(excel_object.getRows()):
    #    row_str = str(row_index+1)
    for col_named in col_named_dict:
        print( col_named, '\n')
        #print( col_named, col_named_dict[col_named])
    #row_str = str(row_index+1)
    #return
    #for row_index in range(1):
    #    row_str = str(row_index+2)
    #    print (row_str, ':\n')
    #    for col_named in col_named_dict:
    #        print( col_named, ':', excel_object.read( col_named_dict[col_named]+row_str))
    #    followed_discussions_tags  = get_tags_set( excel_object.read( col_named_dict['How Can we help you?']+row_str)) + get_tags_set( excel_object.read( col_named_dict['How are you willing to help']+row_str))
    #    print( 'tags:\n', followed_discussions_tags)
    #    for tag in followed_discussions_tags:
    #        print( '<'+tag+'>')
    #return
    
def import_users( excel_file_name, segment_name ):
    excel_object = OpenExcel(excel_file_name)
    col_named_dict = get_col_names_dict(excel_object)
    try:
        segment = Segment.objects.get( title = segment_name)
    except Segment.DoesNotExist:
        print('please create a segment named '+ segment_name)
        return




    all_tags=[]
    for row_index in range(excel_object.getRows()-1):
        row_str = str(row_index+2)
        first_name                 = excel_object.read( col_named_dict['Name']+row_str).strip()
        last_name                  = excel_object.read( col_named_dict['Surename']+row_str).strip()
        email                      = excel_object.read( col_named_dict[u'כתובת אימייל']+row_str).strip()
        education                  = excel_object.read( col_named_dict['Education']+row_str).strip()
        recieve_updates= True
        location_desc              = excel_object.read( col_named_dict['Country? province?']+row_str).strip()
        willing_to_help            = excel_object.read( col_named_dict['How are you willing to help']+row_str).strip()

        if first_name == u'גיא' and last_name == u'דפני':
            first_name = 'Guy'
            last_name = 'Dafny'

        user_name                  = (first_name+'_'+ last_name).casefold().replace(' ', '_').replace(')', '_').replace('(', '_')

        segment                    = segment
        description                = ''
        if willing_to_help:
            willing_to_help=willing_to_help.replace(' (See this Facebook post https://www.facebook.com/groups/614901792606701/permalink/623412731755607/)','')
            description += "I'm willing to help in:" + willing_to_help +  '\r\n'
        if location_desc is 'VA':
            location_desc = 'vankuver'
        if location_desc is 'CA':
            location_desc = 'Canada'
        if location_desc is 'Israel (Living in The Netherlands)':
            location_desc = 'Netherlands'
        if location_desc is 'HaDarom':
            location_desc = 'Israel, South District'

        will_to_share              = excel_object.read( col_named_dict['It can be a good idea to create the links that shall help you/you can help others, Would you mind, sharing your details with other community members ?']+row_str)
        if 'Agree to share my details with other community' in will_to_share:
            social_profile    = excel_object.read( col_named_dict['Social networks profiles,  gitHub, youtube etc']+row_str).strip()
            proffesion        = excel_object.read( col_named_dict['Profession']+row_str).strip()
            want_to_add_that  = excel_object.read( col_named_dict['Anything else that we need to know? Anything to say?']+row_str).strip()
            love_to_do = excel_object.read( col_named_dict['What do you love to do?']+row_str).strip()
            if social_profile:
                description += 'Feel free to follow me on: '+ social_profile + '\r\n'

            if proffesion:
                description += 'I am a '+ proffesion + '\r\n'
            if education:
                description += "I've learned " + education +  '\r\n'
            

            if love_to_do:
                description += 'I most love to '+ love_to_do + '\r\n'
            help_need = excel_object.read( col_named_dict['How Can we help you?']+row_str)
            if help_need:
                help_need=help_need.replace('  (Please submit as a comment  https://www.facebook.com/groups/614901792606701/permalink/623412731755607/)','')

                description += 'I need help in  '+ help_need + '\r\n'
            if want_to_add_that:
                description += 'And '+ want_to_add_that + '\r\n'

        print('\nfirst_name               :',first_name               ,
              '\nlast_name                :',last_name                ,
              '\nemail                    :',email                    ,
              '\nrecieve_updates          :',recieve_updates          ,
              '\ndescription              :',description              ,
              '\nlocation_desc            :',location_desc            ,
              '\nuser_name                :',user_name                ,
              '\nsegment                  :',segment                  ,
              '\nwill_to_share', will_to_share,
              '\nwilling_to_help', willing_to_help,
              '\ndescription              :\n',description)

       # user = create_or_update_kuterless_user(  user_name=user_name, 
        user = create_kuterless_user(  user_name=user_name, 
                                               first_name = first_name, 
                                               last_name = last_name,
                                               email = email,
                                               description = description,
                                               location_desc = location_desc,
                                               segment = segment,
                                               recieve_updates = False)

        
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
Feel free to be one of the first to connect into our system at  http://www.neuronetlabs.org/CoronaVirusHackathon/    \n
1) Your account info:                                                                                                \n
username: {{username}}                                                                                                        \n
This is a link for reset your password: http://www.neuronetlabs.org/reset-password                                   \n
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
Feel free to be one of the first to connect into our system at  http://www.neuronetlabs.org/CoronaVirusHackathon/    \n                                                                                               \n
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








