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

def get_default_email():
    u = User.objects.all()[0]
    return u.email


def get_default_first_name():
    return 'no_first_name'


def get_default_last_name():
    return 'no_last_name'


def create_kuterless_user(  user_name, password, first_name = get_default_first_name(), last_name = get_default_last_name(), email = get_default_email(), recieve_updates = True, description= None, location_desc = None, followed_discussions_tags = None, segment = None):
    
                
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
    user.userprofile.save()
    
    return user



def create_or_update_kuterless_user(  user_name, password, first_name = get_default_first_name(), last_name = get_default_last_name(), email = get_default_email(), recieve_updates = True, description= None, location_desc = None, followed_discussions_tags = None, segment = None):
    user_set = User.objects.filter( username = user_name )
    if user_set.count() != 0:        
        user=user_set[0]
    else:
        user = User(username = user_name)
        init_user_profile(user, segment)
        init_user_account(user)
        init_user_token(user)
    
    user.email=email
    user.first_name=first_name
    user.last_name=last_name
    user.set_password(password)
    user.save()
    user.userprofile.recieve_updates = recieve_updates
    user.userprofile.description = description
    user.userprofile.location_desc = location_desc
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
    for tag_string in tags_string.split(','):
        tagg_to_add =  tag_string.strip().casefold()
        if "willing to join another one's project" not in tagg_to_add:
            tags_set.append(tagg_to_add )
        #print( 'add:','<'+ tag_string.strip().casefold()+'>')
    return tags_set


def delete_all(list):
    for item in list:
        if item.id != None:
            item.delete()

def create_segment( admin_username, password, segment_name):
    segment = Segment(title=segment_name)
    segment.save()
    admin_user = create_kuterless_user( user_name=admin_username, password=password, segment=segment)
    shop = Shop(segment = segment     ,
                admin_user =admin_user,     
                title = segment_name)
    shop.save()
    return segment




    
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
    segment = Segment.objects.get_or_create( title = segment_name)[0]
    shop = Shop.objects.get_or_create( title = segment_name)[0]

    #print( col_named_dict)
    #for row_index in range(excel_object.getRows()):
    #    row_str = str(row_index+1)
    #for col_named in col_named_dict:
    #    print( col_named,  excel_object.read( col_named_dict[col_named]+'2'))
    #    #print( col_named, col_named_dict[col_named])
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
    all_tags=[]
    for row_index in range(excel_object.getRows()-1):
        row_str = str(row_index+2)
        first_name                 = excel_object.read( col_named_dict['Name']+row_str).strip()
        last_name                  = excel_object.read( col_named_dict['Surename']+row_str).strip()
        email                      = excel_object.read( col_named_dict[u'כתובת אימייל']+row_str).strip()
        recieve_updates            = True
        #description                = excel_object.read( col_named_dict['']+row_str).replace(' ', '')
        location_desc              = excel_object.read( col_named_dict['Country? province?']+row_str).strip()
        user_name                  = (first_name+'_'+ last_name).casefold()
        password                   = 'incorrect'
        segment                    = segment
        description                = ''
        will_to_share              = excel_object.read( col_named_dict['It can be a good idea to create the links that shall help you/you can help others, Would you mind, sharing your details with other community members ?']+row_str)
        if 'Agree to share my details with other community' in will_to_share:
            social_profile    = excel_object.read( col_named_dict['Social networks profiles,  gitHub, youtube etc']+row_str).strip()
            proffesion        = excel_object.read( col_named_dict['Profession']+row_str).strip()
            want_to_add_that  = excel_object.read( col_named_dict['Anything else that we need to know? Anything to say?']+row_str).strip()
            love_to_do = excel_object.read( col_named_dict['What do you love to do?']+row_str).strip()
            if social_profile:
                description += 'Feel free to follow me on:'+ social_profile + '\n'

            if proffesion:
                description += 'I am a '+ proffesion + '\n'

            if love_to_do:
                description += 'I most love to '+ love_to_do + '\n'
            help_need = excel_object.read( col_named_dict['How Can we help you?']+row_str)
            if help_need:
                description += 'I need help in  '+ help_need + '\n'
            if want_to_add_that:
                description += 'And '+ want_to_add_that + '\n'
        
    #user = create_or_update_kuterless_user(
    #    first_name      = first_name       ,
    #    last_name       = last_name        ,
    #    email           = email            ,
    #    recieve_updates = recieve_updates  ,
    #    description     = description      ,
    #    location_desc   = location_desc    ,
    #    user_name       = user_name        ,
    #    password        = password         ,
    #    segment         = segment          ,
    #    )                                  

        followed_discussions_tags  = get_tags_set( excel_object.read( col_named_dict['How are you willing to help']+row_str))
        
        print('\nfirst_name               :',first_name               ,
              #'\nlast_name                :',last_name                ,
              #'\nemail                    :',email                    ,
              #'\nrecieve_updates          :',recieve_updates          ,
              #'\ndescription              :',description              ,
              #'\nlocation_desc            :',location_desc            ,
              #'\nuser_name                :',user_name                ,
              #'\npassword                 :',password                 ,
              #'\nsegment                  :',segment                  ,
              '\nwill_to_share', will_to_share,
              '\ndescription              :\n',description,
            )
            #    print( 'tags:\n', followed_discussions_tags)
        for tag in followed_discussions_tags:
            print( '<'+tag+'>')
            if tag not in all_tags:
                all_tags.append(tag)


        print(  '\n\n\n')

    print(  'all tags are:\n')

    for tag in all_tags:
        print( '<'+tag+'>' + '\n')



    return

        #user.userprofile.followed_discussions_tags.clear()
        #for tag in followed_discussions_tags:
        #     user.userprofile.followed_discussions_tags.add(tag)
        #user.userprofile.save()


