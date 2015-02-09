# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
import models
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
import kuterless.settings
from django.template.base import Template
from django.template.context import Context


EMAIL_MAX_SUBJECT_LENGTH = 130 #255 is the limit on some ticketing products (Jira for example) and seems to be the limit on outlook, thunderbird and gmail seem to truncate after 130. –  reconbot Jan 12 '11 at 15:39

def string_to_email_subject( string):
    string = string.replace( "\n", " ").replace( "\r", " ")
    string_size = len(string)
    if string_size > EMAIL_MAX_SUBJECT_LENGTH:
        return string[:EMAIL_MAX_SUBJECT_LENGTH] + '...'
    return string

def send_html_message(subject, html_content, from_email, to_list):
#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_content)
    
    msg = EmailMessage(string_to_email_subject(subject), html_content, from_email, to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def send_html_message_to_users(subject, html_content, to_users_list):
#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_content)
    to_list = []
    for user in to_users_list:
        if user.userprofile.recieve_updates and user.email:
            to_list.append(user.email)
    
    send_html_message(subject, html_content, 'kuterless-no-reply@kuterless.org.il', to_list)


def post_update_to_user(recipient_user_id, header, content = None, discussion_id = None, sender_user_id = None,  details_url = None):
    try:
        recipient_user = User.objects.get(id=recipient_user_id)
    except User.DoesNotExist:
        return

    if not recipient_user.userprofile.recieve_notifications:
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



def get_user_fullname_or_username(user):
    full_name = user.get_full_name()
    if full_name:
        return full_name
    return user.username

def get_user_url(user):
    return reverse('coplay:user_coplay_report', kwargs={'username': user.username})

def user_follow_start_email_updates(follower_user, following_user, inverse_following):

    t = Template("""
        {{follower_user.get_full_name|default:follower_user.username}} התחיל/ה לעקוב אחרי פתיחת הפעילויות שלך
        """)
        
    subject = t.render(Context({"follower_user": follower_user}))

    
    html_message = render_to_string("coplay/user_follow_email_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'follower_user': follower_user,
                                     'html_title': string_to_email_subject(subject),
                                     'details': subject,
                                     'inverse_following': inverse_following})
    

#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_message)
    
    if following_user.email != None and following_user.userprofile.recieve_updates:
        send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [following_user.email])

    post_update_to_user(following_user.id, 
                 header = string_to_email_subject(subject),
                 content = subject, 
                 sender_user_id = follower_user.id,  
                 details_url = reverse('coplay:user_coplay_report', kwargs={'username': follower_user}))


def discussion_email_updates(discussion, subject, logged_in_user, details = None, url_id = '', mailing_list = []):
    if mailing_list == []:
        mailing_list = discussion.get_followers_list()
    allowed_users_list = []
    for user in mailing_list:
        if discussion.can_user_access_discussion( user):
            allowed_users_list.append(user)
         
    html_message = render_to_string("coplay/email_discussion_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'discussion': discussion,
                                     'html_title': string_to_email_subject(subject),
#                                     'subject_debug':string_to_email_subject(subject),
                                     'details': details,
                                     'id': url_id,
                                     'logged_in_user': logged_in_user})
    

#     with open( "duguoutput.html" , "w") as debug_file:
#         debug_file.write(html_message)
    
    for attensdent in allowed_users_list:
        if attensdent != logged_in_user:
            if attensdent.email and attensdent.userprofile.recieve_updates:
                send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [attensdent.email])
            post_update_to_user(attensdent.id, 
                     header = string_to_email_subject(subject),
                     content = details, 
                     sender_user_id = logged_in_user.id,  
                     discussion_id = discussion.id,
                     details_url = reverse('coplay:discussion_details', kwargs={'pk': str(discussion.id)}) + url_id )




def discussion_email_updates_personal(discussion, subject, logged_in_user, details = None, url_id = '', mailing_list = []):
    if mailing_list == []:
        mailing_list = discussion.get_followers_list()
    allowed_users_list = []
    for user in mailing_list:
        if discussion.can_user_access_discussion( user):
            allowed_users_list.append(user)
         
    html_message = render_to_string("coplay/email_discussion_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'discussion': discussion,
                                     'html_title': string_to_email_subject(subject),
#                                     'subject_debug':string_to_email_subject(subject),
                                     'details': details,
                                     'id': url_id,
                                     'logged_in_user': logged_in_user})
    

    with open( "duguoutput.html" , "w") as debug_file:
        debug_file.write(html_message)
    
    for attensdent in allowed_users_list:
        if attensdent != logged_in_user:
            if attensdent.email and attensdent.userprofile.recieve_updates:
                send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [attensdent.email])
            post_update_to_user(attensdent.id, 
                     header = string_to_email_subject(subject),
                     content = details, 
                     sender_user_id = logged_in_user.id,  
                     discussion_id = discussion.id,
                     details_url = reverse('coplay:discussion_details', kwargs={'pk': str(discussion.id)}) + url_id )



def discussion_task_email_updates(task, subject, logged_in_user, details = None):
    attending_list = task.parent.get_followers_list()
    
    allowed_users_list = []
    
    
    for user in attending_list:
        if task.parent.can_user_access_discussion( user):
            allowed_users_list.append(user)

    html_message = render_to_string("coplay/email_task_update.html",
                                    {'ROOT_URL': kuterless.settings.SITE_URL,
                                     'task': task,
                                     'html_title': string_to_email_subject(subject),
#                                     'subject_debug':string_to_email_subject(subject),
                                     'details': details})
    
#    with open( "output.html" , "w") as debug_file:
#        debug_file.write(html_message)

    for attensdent in allowed_users_list:
        if attensdent != logged_in_user:
            if attensdent.email and attensdent.userprofile.recieve_updates:
                send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [attensdent.email])

            post_update_to_user(attensdent.id, 
                     header = string_to_email_subject(subject),
                     content = details, 
                     sender_user_id = logged_in_user.id,  
                     discussion_id = task.parent.id,
                     details_url = reverse('coplay:task_details', kwargs={'pk': str(task.id)}))
    

def task_state_change_update(task, state_change_description):
    t = Template("""
                {{task.responsible.get_full_name|default:task.responsible.username}} {{state_change_description}} :\n
                 "{{task.goal_description}} "\nאושר על ידי {{task.closed_by.get_full_name|default:task.closed_by.username}}
                 """)
                
    trunkated_subject_and_detailes = t.render(Context({"task": task, 'state_change_description': state_change_description}))


                
    discussion_task_email_updates(  task,
                                    trunkated_subject_and_detailes,
                                    task.closed_by,
                                    trunkated_subject_and_detailes)



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



def user_glimpsed_another_user_s_discussion( user, discussion , views_counter = 0):
            
    t = Template("""
    {{user.get_full_name|default:user.username}} צפה/תה בפעילות שלך "{{discussion.title}}" בפעם ה {{views_counter}}
    """)
    
#     t = Template("""
#     צפה/תה ב "{{discussion.title}}" בפעם ה {{views_counter}}
#     """)    
    trunkated_subject_and_detailes = t.render(Context({"discussion": discussion,
                                                       'user': user,
                                                       'views_counter': views_counter}))
                                                        
    mailing_list = []
    mailing_list.append(discussion.owner)

    discussion_email_updates(   discussion = discussion, 
                                 subject = trunkated_subject_and_detailes, 
                                 logged_in_user = user, 
                                 details = trunkated_subject_and_detailes, 
                                 url_id = '', 
                                 mailing_list = mailing_list)

    user.account.deposit_and_return_transaction_if_ok( title = u"צפיה בפעילות של מישהו אחר", 
                                                       positive_item_price = 2, 
                                                       url = discussion.get_absolute_url()) 
    
def init_user_profile(user, segment = None):
    user.userprofile = models.UserProfile(user = user, segment = segment)
    user.userprofile.save()
    user.save()    
    
