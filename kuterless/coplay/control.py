# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""
from coplay.models import UserProfile, Discussion, MAX_TEXT,  \
    UserUpdate
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.core.validators import MaxLengthValidator
from django.db import models



def get_all_users_visiabale_for_a_user_list(user_id_or_none_when_anoynymous = None):
    if user_id_or_none_when_anoynymous != None:
        try:
            known_user = User.objects.get(id=user_id_or_none_when_anoynymous)
        except User.DoesNotExist:
            return []
        return known_user.userprofile.get_all_users_in_same_segment_list()
    all_users_visiabale_for_a_user_list = []
    for user_profile in UserProfile.objects.all():
        if user_profile.segment == None:
            all_users_visiabale_for_a_user_list.append(user_profile.user)
            
    return all_users_visiabale_for_a_user_list


def post_update_to_user(recipient_user_id, header, content = None, discussion_id = None, sender_user_id = None,  details_url = None):
    try:
        recipient_user = User.objects.get(id=recipient_user_id)
    except User.DoesNotExist:
        return

    if discussion_id:
        try:
            discussion = Discussion.objects.get(id=discussion_id)
        except Discussion.DoesNotExist:
            return
    else:
        discussion = None
    
    if sender_user_id:
        try:
            sender_user = User.objects.get(id=sender_user_id)
        except User.DoesNotExist:
            return
    else:
        sender_user = None
       

    user_update = UserUpdate(
        discussion =discussion, 
        recipient = recipient_user,
        sender = sender_user,
        header = header,
        content = content,
        details_url = details_url)
    user_update.clean()
    user_update.save()

    
