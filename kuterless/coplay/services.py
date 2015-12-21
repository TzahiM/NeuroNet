# -*- coding: utf-8 -*-
from coplay.control import user_glimpsed_another_user_s_discussion, \
    anonymous_user_increment_views_counter, discussion_task_email_updates, \
    task_state_change_update, discussion_email_updates, \
    user_started_a_new_discussion, user_follow_start_email_updates, \
    string_to_email_subject, send_html_message, post_update_to_user, \
    user_posted_a_feedback_in_another_other_user_s_discussion, \
    user_post_a_decision_for_vote_regarding_his_own_discussion, \
    user_voted_for_an_idea_in_another_user_s_discussion, \
    user_completed_a_mission_for_his_own_s_discussion, \
    user_completed_a_mission_for_another_user_s_discussion, \
    user_aborted_a_mission_for_his_own_s_discussion, \
    user_aborted_a_mission_for_another_user_s_discussion, \
    user_confirmed_a_state_update_in_another_user_s_mission, \
    poll_for_task_complition
from coplay.models import Task, Discussion, FollowRelation, AnonymousVisitor, \
    Feedback, MAX_INACTIVITY_SECONDS, Decision, LikeLevel, Vote, UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import timezone
import kuterless.settings

MAX_MESSAGE_INPUT_CHARS = 900

def get_accessed_list( all_objects_list, user = None):
    returned_list = []
    for item in all_objects_list:
        if can_user_acess_discussion( item.get_discussion(), user):
            returned_list.append(item)
    
    return returned_list
    
    
def is_in_the_same_segment(user , another_user = None ):
    segment = None
    if user.is_authenticated():
        segment = user.userprofile.segment
    
    tested_segment = None
    if another_user.is_authenticated():
        tested_segment = another_user.userprofile.segment
        
    return ( segment == tested_segment)

def get_all_users_visiabale_for_a_user_list(user = None):
    segment = None
    if user != None and user.is_authenticated():
        segment = user.userprofile.segment
    
    all_users_visiabale_for_a_user_list = []
    for user_profile_iterator in UserProfile.objects.all():
        if user_profile_iterator.segment == segment:
            all_users_visiabale_for_a_user_list.append(user_profile_iterator.user)
            
    if user != None and user.is_authenticated():
        all_users_visiabale_for_a_user_list.remove(user)
    
    return all_users_visiabale_for_a_user_list

def can_user_acess_discussion(discussion, user):
    if not user.is_authenticated():
        return discussion.can_user_access_discussion(None)
    
    return discussion.can_user_access_discussion(user)

def discussion_record_a_view( discussion, user ):
    
    if user.is_authenticated() == False:
        return False , 'user is not authenticated'
    
    if not discussion.can_user_access_discussion( user):
        return False, 'user cannot access discussion'
    
    viewer = discussion.viewer_set.get_or_create( user = user)[0]
    if viewer.discussion_updated_at_on_last_view != viewer.discussion.updated_at: 
        viewer.views_counter += 1            
        viewer.discussion_updated_at_on_last_view = viewer.discussion.updated_at
        glimpse = viewer.glimpse_set.create( viewer = viewer)
        glimpse.clean()
        glimpse.save()
        if viewer.user != viewer.discussion.owner:
            user_glimpsed_another_user_s_discussion( user = viewer.user, 
                                                     discussion     = viewer.discussion, 
                                                     views_counter  = viewer.views_counter)
        
    viewer.views_counter_updated_at = timezone.now()
    viewer.save()
        
    return True, None

def discussion_record_anonymous_view(discussion, request):
    
    if 'anonymous_user_id' in request.session:
        if AnonymousVisitor.objects.filter( id = int(request.session['anonymous_user_id'])).count() != 0:
            anonymous_user = AnonymousVisitor.objects.get( id = int(request.session['anonymous_user_id']))
        else:
            anonymous_user = AnonymousVisitor()
            anonymous_user.save()
        
        anonymous_viewer = discussion.anonymousvisitorviewer_set.get_or_create( anonymous_visitor = anonymous_user)[0]
        
        if request.user.is_authenticated():
            anonymous_user.user = request.user;
            anonymous_user.save()
        else:
            if anonymous_viewer.discussion_updated_at_on_last_view != anonymous_viewer.discussion.updated_at: 
                anonymous_viewer.views_counter += 1            
                anonymous_viewer.discussion_updated_at_on_last_view = anonymous_viewer.discussion.updated_at
                glimpse = anonymous_viewer.glimpse_set.create( anonymous_visitor_viewer = anonymous_viewer)
                glimpse.clean()
                glimpse.save()            
            
            
            
            
            
            
            
            
            
            
    else:
        if request.user.is_authenticated():
            return
        anonymous_user = AnonymousVisitor()
        anonymous_user.save()
        anonymous_viewer = discussion.anonymousvisitorviewer_set.get_or_create( anonymous_visitor = anonymous_user)[0]
        anonymous_user_increment_views_counter( anonymous_viewer)
        
    
    request.session['anonymous_user_id'] = anonymous_user.id

            

def update_task_status_description( task , description, user):
        
    if user is None:
        return None, 'no user provided'
    
    if description is None:
        return None, 'no description'

    if user != task.responsible:
        return None, 'only the responsible can update the description'
    
    poll_for_task_complition( task)
    if( task.final_state):
        return None, 'target date passed'
        
    task.status_description = description
    task.save()
    
    task.parent.save()#verify that the entire disscusion is considered updated
    
    t = Template("""
    {{task.responsible.get_full_name|default:task.responsible.username}} הודיע/ה ש :\n
    "{{task.get_status_description}} "\n
    """)
    
    trunkated_subject_and_detailes = t.render(Context({"task": task}))
    
    discussion_task_email_updates(task,
                                  trunkated_subject_and_detailes,
                                  user,
                                  trunkated_subject_and_detailes)
        
    return task, None


def update_task_state( task , new_state , user ):

    if new_state != Task.STARTED and new_state != Task.CLOSED and new_state != Task.ABORTED:
        return None, 'unknown task state ' + str(new_state)
    
    if not task.parent.can_user_access_discussion( user):
        return None, 'user cannot access discussion'


    if user == task.responsible:
        return None, 'responsible can not update task status'

    poll_for_task_complition( task)

    if task.final_state:
        return None, 'target date passed'
    
    if (task.status != new_state):
        task.status = new_state
        task.closed_at = timezone.now()
        task.closed_by = user
        task.save()
    
        task.parent.save() #verify that the entire discussion is considered updated            

   
        success, error_string = start_discussion_following( task.parent, user)
        
        if success == False:
            return None, error_string
        
        if new_state == task.STARTED:
            task_state_change_update( task,  u" עדיין לא השלים/ה את ")
            
        if new_state == task.ABORTED:
            task_state_change_update( task,  u" ביטל/ה את ")
    
        if new_state == task.CLOSED:
            task_state_change_update( task,  u" השלימ/ה את ")

    return task, None

        

def discussion_update( discussion, user, description, 
                       tags_string = None, 
                       location_desc = None, 
                       parent_url = None,
                       parent_url_text = None):
    
    if user != discussion.owner:
        return None, 'only owner can update discussion'
    
    if not discussion.is_active():
        return None, 'discussion is locked'

    print tags_string
    
    discussion.description   = description
    discussion.location_desc = location_desc
    discussion.parent_url = parent_url
    discussion.parent_url_text = parent_url_text
    tags_list =  tags_string.split(',')
    for tag in tags_list:
        discussion.tags.add( tag)
        
    discussion.description_updated_at = timezone.now()
    discussion.save()#cause all previous fedbacks to be striked at

    for tag in discussion.tags.all():
        start_tag_following(user, tag)
        
    start_discussion_following( discussion, user)
    

    t = Template("""
    {{discussion.owner.get_full_name|default:discussion.owner.username}} עידכן/ה את המטרות של הפעילות והעזרה המבוקשת :\n
    "{{discussion.description}} "\n
    """)
    
    trunkated_subject_and_detailes = t.render(Context({"discussion": discussion}))
                                                        

    discussion_email_updates(discussion,
                             trunkated_subject_and_detailes,
                             user,
                             trunkated_subject_and_detailes)
    
    return discussion, None



def create_discussion( user             = None, 
                       title            = None, 
                       description      = None,                       
                       location_desc    = None,                       
                       tags_string      = None,
                       parent_url       = None,
                       parent_url_text  = None,
                       latitude         = 0.0,
                       longitude        = 0.0):
    if user is None:
        return None, 'no user provided'
    
    if user.is_authenticated() is False:
        return None, 'user not authenticated'

    if title is None:
        return None, 'Title not provided'

    if description is None:
        return None, 'description not provided'
    
    if len(description) > MAX_MESSAGE_INPUT_CHARS:
        return None, 'description len ' + str(len(description)) + '>' + str(MAX_MESSAGE_INPUT_CHARS)
        

    discussions_list = Discussion.objects.all().filter(owner=user,
                                                       title = title )
    
    if discussions_list.count() != 0:
        return None, 'user posted a discussion with the same title'

    new_discussion = Discussion(    owner           =  user,
                                    title           = title,
                                    description     = description,
                                    parent_url      = parent_url,
                                    parent_url_text = parent_url_text,
                                    latitude        = latitude,
                                    longitude       = longitude)
    if location_desc:
        new_discussion.location_desc = location_desc
                
    new_discussion.clean()
    new_discussion.save()
    if tags_string:
        tags_list =  tags_string.split(',')
        for tag in tags_list:
            new_discussion.tags.add( tag)
            
                                
    new_discussion.full_clean()
    new_discussion.description_updated_at = timezone.now()
    new_discussion.save()

    user_started_a_new_discussion( new_discussion.owner)
    start_discussion_following(new_discussion, user)
    for tag in new_discussion.tags.all():
        start_tag_following( user, tag)
            
    t = Template("""
    {{discussion.owner.get_full_name|default:discussion.owner.username}} ביקש/ה את העזרה שלך ב :
    "{{discussion.title}} "\n
    """)
            
    trunkated_subject_and_detailes = t.render(Context({"discussion": new_discussion}))

    new_discussion_followers = []

    user_s_following = get_followers_list(new_discussion.owner)
    
#all the followers for the user and all the followers for a tag
     
    for user in User.objects.all():
        if new_discussion.can_user_access_discussion( user):
            if user in user_s_following:
                new_discussion_followers.append(user)
            else:
                to_append = False
                for tag_iter in user.userprofile.followed_discussions_tags.all():
                    if tag_iter.name in new_discussion.tags.names():
                        to_append = True
                if to_append:
                    new_discussion_followers.append(user)
    
          
    discussion_email_updates(new_discussion,
                             trunkated_subject_and_detailes,
                             new_discussion.owner,
                             trunkated_subject_and_detailes,
                             mailing_list = new_discussion_followers )
    
    return new_discussion, None


def start_users_following( follower_user, following_user):
    
    if follower_user == following_user:
        return
    

    already_following = is_user_is_following( follower_user, following_user)
    
    inverse_following = is_user_is_following(following_user ,  follower_user )

    FollowRelation.objects.get_or_create( follower_user = follower_user, following_user = following_user)
    
    if not already_following:
        user_follow_start_email_updates(follower_user, following_user, inverse_following)
     

def stop_users_following( follower_user, following_user):
    if FollowRelation.objects.filter( follower_user = follower_user, following_user = following_user).count() != 0:
        deleted_follow_relation = FollowRelation.objects.get( follower_user = follower_user, following_user = following_user) 
        deleted_follow_relation.delete()

def start_tag_following( follower_user, tag):
        
    if False == ( tag in follower_user.userprofile.followed_discussions_tags.all()):
            
        follower_user.userprofile.followed_discussions_tags.add( tag.name)
        follower_user.userprofile.save()
        
        all_users_visiabale_for_a_user_list = get_all_users_visiabale_for_a_user_list(follower_user)
#         already_following_users = []
        
#         for user in all_users_visiabale_for_a_user_list:
#             if name in user.userprofile.followed_discussions_tags.names():
#                 already_following_users.append(user)

        t = Template("""
            {{follower_user.get_full_name|default:follower_user.username}} גם התחיל/ה לעקוב אחרי {{name}}
            """)
        subject = t.render(Context({"follower_user": follower_user,
                                    "name" : tag.name}))
        
        html_message = render_to_string("coplay/user_follow_tag_email_update.html",
                                        {'ROOT_URL': kuterless.settings.SITE_URL,
                                         'follower_user': follower_user,
                                         'html_title': string_to_email_subject(subject),
                                         'details': subject,
                                         'tag': tag})

#         with open( "output.html" , "w") as debug_file:
#             debug_file.write(html_message)
            
        for user in all_users_visiabale_for_a_user_list:
            if tag in user.userprofile.followed_discussions_tags.all():
                if user.email != None and user.userprofile.recieve_updates:
                    send_html_message(subject, html_message,
                              'kuterless-no-reply@kuterless.org.il',
                              [user.email])
                post_update_to_user(user.id, 
                                    header = string_to_email_subject(subject),
                                    content = subject, 
                                    sender_user_id = follower_user.id,  
                                    details_url = reverse('coplay:discussion_tag_list', kwargs={'pk': tag.id}))

def stop_tag_following( follower_user, tag):

    if follower_user == None or follower_user.is_authenticated() == False:
        return 
    
    follower_user.userprofile.followed_discussions_tags.remove( tag.name)
    follower_user.userprofile.save()


def start_discussion_following( discussion, following_user):
    
    if following_user == None or following_user.is_authenticated() == False:
        return None, "not authenticated"
    
    if not discussion.can_user_access_discussion(following_user):
        return None, "user cannot access discussion"
    
    viewer = discussion.viewer_set.get_or_create( user = following_user)[0]
    viewer.is_a_follower = True
    viewer.save()

    return discussion, None


def stop_discussion_following( discussion, following_user):
    
    if following_user == None or following_user.is_authenticated() == False:
        return False, "not authenticated"
        
    if not discussion.can_user_access_discussion(following_user):
        return False, "user cannot access discussion"
    
    viewer = discussion.viewer_set.get_or_create( user = following_user)[0]
    viewer.is_a_follower = False
    viewer.save()
    
    return True, None
    

def discussion_add_feedback(discussion, user, feedbabk_type = None, content = None):
    if feedbabk_type == None:
        return None, 'No feedback type'
    
    if feedbabk_type != Feedback.ADVICE and feedbabk_type != Feedback.COOPERATION and feedbabk_type != Feedback.INTUITION and feedbabk_type != Feedback.ENCOURAGE:
        return None,(  'Wrong feedback type ' + str(feedbabk_type))

    if False == discussion.can_user_access_discussion(user):
        return None, "user cannot access discussion"
    
#     if not discussion.is_active():
#         return None, "discussion is not active"
            
    if user == discussion.owner:
        return None, "discussion owner cannot post a feedback"
    
    if Feedback.objects.filter( discussion = discussion, feedbabk_type = feedbabk_type, content = content, user = user).count() != 0:
        return None, "feedback already exists"
    
    feedback = Feedback(discussion=discussion, user=user,
                        feedbabk_type=feedbabk_type, content=content)
    feedback.full_clean()
    feedback.save()
    discussion.save() #verify that the entire discussion is considered updated
    
    
    success, error_string = start_discussion_following( discussion, user)
    
    if success == False:
        return None, error_string
    
    t = Template("""
    {{feedbabk.user.get_full_name|default:feedbabk.user.username}} פירסם/ה {{feedbabk.get_feedbabk_type_name}}:\n
    "{{feedbabk.content}} "\n
    """)

    trunkated_subject_and_detailes = t.render(Context({"feedbabk": feedback}))
                                                        
    discussion_email_updates(discussion,
                             trunkated_subject_and_detailes,
                             user,
                             trunkated_subject_and_detailes)           
     
        
    
    user_posted_a_feedback_in_another_other_user_s_discussion(user, feedback.get_absolute_url())
    
    return feedback, None
    
def discussion_add_task(discussion, responsible, goal_description, target_date,
                        max_inactivity_seconds=MAX_INACTIVITY_SECONDS):

    if not discussion.can_user_access_discussion(responsible):
        return None, "user cannot access discussion"
    
    if target_date <= timezone.now():
        return None, "target date should be in the future"
        
    tasks_list = Task.objects.all().filter(responsible=responsible,
                                           goal_description=  goal_description,
                                           parent=discussion)
    if tasks_list.count() != 0:
        return None, "task already exsist"
        
    task = discussion.task_set.create(parent=discussion, responsible=responsible,
                                    goal_description=goal_description,
                                    target_date=target_date)
    task.full_clean()
    task.save()
    discussion.unlock(max_inactivity_seconds)
    discussion.save() #verify that the entire discussion is considered updated
    start_discussion_following( discussion, responsible)
    t = Template("""
            {{task.responsible.get_full_name|default:task.responsible.username}} הבטיח/ה ש :\n
            "{{task.goal_description}} "\n  עד {{task.target_date | date:"d/n/Y H:i"}}
            """)
            
   
    success, error_string = start_discussion_following( discussion, responsible)
    
    if success == False:
        return None, error_string
            
    trunkated_subject_and_detailes = t.render(Context({"task": task}))
    discussion_task_email_updates(task,
                                 trunkated_subject_and_detailes,
                                 responsible,
                                 trunkated_subject_and_detailes)
    
    return task, None


def discussion_add_decision(discussion, user, content = None):
    if content == None:
        return None, 'No content'

    if not discussion.is_active():
        return None, "discussion is not active"
            
    if user != discussion.owner:
        return None, "only discussion add a desicion"
    
    if Decision.objects.filter( parent = discussion, content = content).count() != 0:
        return None, "decision already exists"

    decision = Decision(parent=discussion, content=content)
    decision.full_clean()
    decision.save()
    discussion.save() #verify that the entire discussion is considered updated
        
   
    success, error_string = start_discussion_following( discussion, user)
    
    if success == False:
        return None, error_string

    t = Template("""
    {{decision.parent.owner.get_full_name|default:decision.parent.owner.username}} מבקש/ת שתצביע/י על :\n
    "{{decision.content}} "\nלהצבעה צריך להיכנס אל הפעילות המלאה...
    """)
    
    trunkated_subject_and_detailes = t.render(Context({"decision": decision}))
    
    discussion_email_updates(discussion,
                             trunkated_subject_and_detailes,
                             user,
                             trunkated_subject_and_detailes,
                             "#Decisions")
    
    user_post_a_decision_for_vote_regarding_his_own_discussion( user, decision.get_absolute_url())
    
    return decision, None



def discussion_invite(discussion, user = None):
            
    if user == discussion.owner:
        return None, "discussion owner is always invited"
    
    if not discussion.is_user_in_discussion_segment(user):
        return None ,"user cannot access discussion"
    
    viewer = discussion.viewer_set.get_or_create( user = user)[0]
    viewer.is_invited = True
    viewer.save()
    
    return discussion, None


def discussion_cancel_invite(discussion, user = None):
            
    if user == discussion.owner:
        return None, "discussion owner is alwaye invited"
    
    if not discussion.can_user_access_discussion(user):
        return None, "user cannot access discussion"
    
    viewer = discussion.viewer_set.get_or_create( user = user)[0]
    viewer.is_invited = False
    viewer.save()
    
    return discussion, None



def decision_vote(decision, user, value = None):
    
    if value == None:
        return False, 'missing vote value'
        
    if value != LikeLevel.BAD and value != LikeLevel.MEDIUM and value != LikeLevel.GOOD and value != LikeLevel.VERY_GOOD and value != LikeLevel.EXCELLENT:
        return False,  'Wrong vote value ' + str(value)

    if False ==  decision.parent.can_user_access_discussion( user):
        return False,  "user cannot access discussion"

#     if not decision.parent.is_active():
#         return False,  "discussion is not active"
            
    if user == decision.parent.owner:
        return False, False,"discussion owner cannot vote"
    
    first_vote = (decision.vote_set.filter(voater=user).count() == 0)

    if first_vote:
        new_vote = Vote(decision = decision, voater=user, value=value)
        new_vote.save()
        decision.value += value
        decision.save()
        user_voted_for_an_idea_in_another_user_s_discussion( user , decision.get_absolute_url())
    else:
        current_vote = decision.vote_set.get(voater=user)
        decision.value -= current_vote.value
        current_vote.value = value
        decision.value += current_vote.value
        current_vote.save()
        decision.save()
 
   
    success, error_string = start_discussion_following( decision.parent, user)
    
    if success == False:
        return False, error_string
        
    return True, None


    
def is_user_is_following( follower_user, following_user):
    return FollowRelation.objects.filter( follower_user = follower_user, following_user = following_user).count() != 0

    

def get_followers_list( following_user):
    
    followers_list = []
    
    follow_relations_set = FollowRelation.objects.filter( following_user = following_user)
    
    for follow_relations in follow_relations_set:
        followers_list.append(follow_relations.follower_user)
        
    return followers_list

def get_following_list( follower_user):
    
    following_list = []
    
    follow_relations_set = FollowRelation.objects.filter( follower_user = follower_user)
    
    for follow_relations in follow_relations_set:
        following_list.append(follow_relations.following_user)
        
    return following_list

    

def get_user_fullname_or_username(user):
    full_name = user.get_full_name()
    if full_name:
        return full_name
    return user.username
        
      


def task_get_status( task):

    poll_for_task_complition( task)
    
    return task.status

