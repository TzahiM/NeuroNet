# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User
import models


def get_all_users_visiabale_for_a_user_list(user_id_or_none_when_anoynymous = None):
    if user_id_or_none_when_anoynymous != None:
        try:
            known_user = User.objects.get(id=user_id_or_none_when_anoynymous)
        except User.DoesNotExist:
            return []
        return known_user.userprofile.get_all_users_in_same_segment_list()
    all_users_visiabale_for_a_user_list = []
    for user_profile in models.UserProfile.objects.all():
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
            discussion = models.Discussion.objects.get(id=discussion_id)
        except models.Discussion.DoesNotExist:
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
       

    user_update = models.UserUpdate(
        discussion =discussion, 
        recipient = recipient_user,
        sender = sender_user,
        header = header,
        content = content,
        details_url = details_url)
    user_update.clean()
    user_update.save()



def user_started_a_new_discussion( user, url = None):

    user.account.deposit_and_return_transaction_if_ok( u"התחיל פעילות חדשה", 
    positive_item_price = 27, url = url)
    

def user_completed_a_mission_for_another_user_s_discussion( user, url = None):

    user.account.deposit_and_return_transaction_if_ok( u"השלים משימה  בשביל  משתתף אחר",
                                                  positive_item_price = 23, url = url)


def user_aborted_a_mission_for_another_user_s_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok( u"ביטול משימה בשביל משתתף אחר",
                                                  positive_item_price = 19, url = url)



def user_completed_a_mission_for_his_own_s_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok( "השלים משימה  לקידום פעילות שלו ",
                                                  positive_item_price = 17, url = url)



def user_aborted_a_mission_for_his_own_s_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok( u"ביטול משימה שלקח לטובת פעילות שלו ",
                                                  positive_item_price = 13, url = url)

     
def user_confirmed_a_state_update_in_another_user_s_mission( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok( u"אישור עדכון של מצב משימות",
                                                  positive_item_price = 11, url = url)



def user_posted_a_feedback_in_another_other_user_s_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok( u"תגובה בפעילות של משתתף אחר", 
                                                        positive_item_price = 7, url = url)

def user_post_a_decision_for_vote_regarding_his_own_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok(u"העלאת רעיון להצבעה", 
                                                  positive_item_price = 5, url = url) 


def user_voted_for_an_idea_in_another_user_s_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok(u"הצבעה על רעיון של משתתף אחר", 
                                                  positive_item_price = 3, url = url) 



def user_glimpsed_another_user_s_discussion( user, url = None):
    
    user.account.deposit_and_return_transaction_if_ok( title = u"צפיה בפעילות של מישהו אחר", 
                                                  positive_item_price = 2, url = url) 
    
def init_user_profile(user, segment = None):
    user.userprofile = models.UserProfile(user = user, segment = segment)
    user.userprofile.save()
    user.save()    
    
    
