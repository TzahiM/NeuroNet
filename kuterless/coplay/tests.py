# -*- coding: utf-8 -*-
from coplay import api
from coplay.control import init_user_profile, post_update_to_user, \
    user_started_a_new_discussion
from coplay.models import Discussion, Feedback, Decision, LikeLevel, Vote, Task, \
    FollowRelation, Segment, UserUpdate, Glimpse
from coplay.serializers import CreateFeedback
from coplay.views import is_user_is_following, start_users_following, \
    stop_users_following, get_followers_list, get_following_list
from django.contrib.auth.models import User
from django.core.serializers import json
from django.test import TestCase
from django.utils import timezone
from memecache.control import init_user_account
from memecache.models import Account
from public_fulfillment.control import create_kuterless_user, simple_auth_token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.test import APIRequestFactory, force_authenticate
import datetime
import time




class CoPlayTest(TestCase):
    
#     def setUp(self):
#         
#         self.factory = APIRequestFactory()
#         self.admin = create_kuterless_user('admin', '1234','john', 'doo','user1@example.com',False)
# 
#         self.at1 = create_kuterless_user('at1', '1234','john', 'doo','user1@example.com',False)
# 
# 
#     def create_dicussion(self):
#         d = Discussion( owner = self.admin, title = "Visit the moon")
#         user_started_a_new_discussion( d.owner)
#         d.full_clean()
#         d.save()
#         return d
#         
#     def create_user(self):
#         
#         self.user = create_kuterless_user('zugu', '1234', 'john', 'doo', 'ee@dd.com', False)
#         
#         
#         
#     def test_api_add_feedback(self):
#         
#         self.create_user()
# 
#         d = self.create_dicussion()
#  
#         pk = str(d.id)
# #        request = self.factory.post('/labs/coplay/api/create_feedback/' + pk, {'feedback_type':2,  'content':  'sssss'}, format='json')
# #        request = self.factory.post('/labs/coplay/api/create_feedback/' + pk,{"feedback_type":2,  "content":  "sssss"}, content_type='application/json')
#         request = self.factory.post('/labs/coplay/api/create_feedback/' + pk,{"content": "ggg2",  "feedback_type":  2 }, content_type='application/json')
#         request.user = self.at1
#         print 'fff'
#         print request.body
#         view = api.AddFeedBackView()
#         response = api.AddFeedBackView.post(view, request, pk)
#         print response.data   
#         if Feedback.objects.count() == 1:
#             Feedback.objects.first().print_ocntent()
#                 
        

    def setUp(self):
        self.admin = User.objects.create_user('admin', 'user1@example.com',
                                              'secret')
        self.at1 = User.objects.create_user('at1', 'user1@example.com',
                                              'secret')
        self.at2 = User.objects.create_user('at2', 'user1@example.com',
                                              'secret')
        self.at3 = User.objects.create_user('at3', 'user1@example.com',
                                              'secret')
        
        self.at4 = User.objects.create_user('at4', 'user1@example.com',
                                              'secret')
        self.at5 = User.objects.create_user('at5', 'user1@example.com',
                                              'secret')
        self.at6 = User.objects.create_user('at6', 'user1@example.com',
                                              'secret')
        
        
        
        
        init_user_profile(self.admin)
        init_user_profile(self.at1)
        init_user_profile(self.at2)
        init_user_profile(self.at3)
        init_user_profile(self.at4)
        init_user_profile(self.at5)
        init_user_profile(self.at6)
        
        init_user_account(self.admin)
        init_user_account(self.at1)
        init_user_account(self.at2)
        init_user_account(self.at3)
        init_user_account(self.at4)
        init_user_account(self.at5)
        init_user_account(self.at6)
        


    def create_dicussion(self):
        d = Discussion( owner = self.admin, title = "Visit the moon")
        user_started_a_new_discussion( d.owner)
        d.full_clean()
        d.save()
        return d

    def create_feedback(self):
        d = Feedback()
        d.discussion = self.admin
        d.title = "Visit the moon"
        d.full_clean()
        d.save()
        return d
    
    def test_create_discussion(self):
        self.assertEquals(0, Discussion.objects.count())
        d = self.create_dicussion()
        self.assertEquals(1, Discussion.objects.count())
        d.print_content()

    def test_update_description(self):
        new_description = 'i have another idea'
        d = self.create_dicussion()
        d.update_description( new_description)
        d.save()
        self.assertEquals(new_description, d.description)
        


    def test_add_feedback(self):
        self.assertEquals(0, Feedback.objects.count())
        d = self.create_dicussion()
        d.add_feedback(self.at1, Feedback.ENCOURAGE, "like this")
        d.add_feedback(self.at1, Feedback.ENCOURAGE, "like this")
        d.add_feedback(self.at1, Feedback.COOPERATION, "COOPERATION this")
        d.add_feedback(self.at1, Feedback.COOPERATION, "like COOPERATION")
        d.add_feedback(self.at1, Feedback.INTUITION, "INTUITION this")
        d.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        d.add_feedback(self.at1, Feedback.ADVICE, "ADVICE this")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICE")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICEADVICE")
        self.assertEquals(9, Feedback.objects.count())
        d.print_content()


    def test_decision(self):
        self.assertEquals(0, Decision.objects.count())
        d = self.create_dicussion()
        des = d.add_decision( 'content')
        self.assertEquals(1, Decision.objects.count())
        self.assertEquals(0, Vote.objects.count())
        des.vote( self.at1 ,  LikeLevel.EXCELLENT)
        des.vote( self.at1 ,  LikeLevel.BAD)
        des.vote( self.at2 ,  LikeLevel.GOOD)
        self.assertEquals(2, Vote.objects.count())
        self.assertEquals(2, des.get_number_of_votes())
        self.assertEquals(4, des.get_vote_sum())
        self.assertEquals( des.get_vote_value_or_none( self.at2) , LikeLevel.GOOD )
        self.assertEquals( des.get_vote_value_or_none( self.at3) , None )
        d.print_content()

    def test_action(self):    
        self.assertEquals(0, Task.objects.count())
        d = self.create_dicussion()
        task1 = d.add_task(self.at1, 'shall start', timezone.now() +  datetime.timedelta(seconds =4))
        task2 = d.add_task(self.at2, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        task3= d.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        task4 = d.add_task(self.at2, 'shall abort', timezone.now() +  datetime.timedelta(seconds =2))
        task5 = d.add_task(self.at2, 'shall abort and tnan closed', timezone.now() +  datetime.timedelta(seconds =2))
        task6 = d.add_task(self.at2, 'shall abort and tnan reopen', timezone.now() +  datetime.timedelta(seconds =2))
        task7 = d.add_task(self.at2, 'shall closed and tnan reopen', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(7, Task.objects.count())
        time.sleep(1)
        task2.close(self.admin)
        task4.abort(self.admin)
        task5.abort(self.admin)
        task5.close(self.admin)
        task6.abort(self.admin)
        task6.re_open(self.admin)
        self.assertEquals(task6.STARTED, task6.get_status())
        task7.close(self.admin)
        task7.re_open(self.admin)
        self.assertEquals(task7.STARTED, task7.get_status())
        time.sleep(2)
        self.assertEquals(self.admin, task2.closed_by)
        self.assertEquals(self.admin, task4.closed_by)
        self.assertEquals(False, task1.close(self.at1))
        self.assertEquals(task1.STARTED, task1.get_status())
        self.assertEquals(task1.CLOSED, task2.get_status())
        self.assertEquals(task1.MISSED, task3.get_status())
        self.assertEquals(task1.ABORTED, task4.get_status())
        self.assertEquals(task1.CLOSED, task5.get_status())
        self.assertEquals(task1.MISSED, task6.get_status())
        self.assertEquals(task1.MISSED, task7.get_status())
                        
        new_stat_desc = "fjfj"
        self.assertEquals( True, task1.update_status_description(new_stat_desc))
        self.assertEquals(task1.get_status_description(), new_stat_desc)
        new_stat_desc = "dfasgg"
        task1.close(self.admin)
        time.sleep(2)
        task1.update_status_description(new_stat_desc)
        self.assertNotEquals(task1.get_status_description(), new_stat_desc)
        d.print_content()
        

        
        

    def test_whole_discussion(self):    
        d = self.create_dicussion()
        d.add_feedback(self.at1, Feedback.ENCOURAGE, "like this")
        d.add_feedback(self.at2, Feedback.ENCOURAGE, "like this")
        d.add_feedback(self.at3, Feedback.COOPERATION, "COOPERATION this")
        d.add_feedback(self.at3, Feedback.COOPERATION, "like COOPERATION")
        d.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        d.add_feedback(self.at3, Feedback.ADVICE, "ADVICE this")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICE")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICEADVICE")
        
        
        des1 = d.add_decision( 'אולי מלמטה?')
        des1.vote( self.at1 ,  LikeLevel.EXCELLENT)
        des1.vote( self.at1 ,  LikeLevel.BAD)
        des1.vote( self.at2 ,  LikeLevel.MEDIUM)
        des1.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        des1.vote( self.at3 ,  LikeLevel.BAD)
        d.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        task2 = d.add_task(self.at2, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        task3= d.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        task2.close(self.admin)
        des2 = d.add_decision( 'אולי מלמעלה?')
        des2.vote( self.at1 ,  LikeLevel.BAD)
        des2.vote( self.at2 ,  LikeLevel.MEDIUM)
        des2.vote( self.at2 ,  LikeLevel.VERY_GOOD)        

        d2 = self.create_dicussion()
        d2.add_feedback(self.at3, Feedback.COOPERATION, "COOPERATION this")
        d2.add_feedback(self.at3, Feedback.COOPERATION, "like COOPERATION")
        d2.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d2.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        des3 = d2.add_decision( 'אולי מלמטה?')
        des3.vote( self.at1 ,  LikeLevel.EXCELLENT)
        des3.vote( self.at1 ,  LikeLevel.BAD)
        des3.vote( self.at2 ,  LikeLevel.MEDIUM)
        des3.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        des3.vote( self.at3 ,  LikeLevel.BAD)
        d2.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d2.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        task4 = d.add_task(self.at2, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        task5= d.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        task4.close(self.admin)
        des2 = d2.add_decision( 'אולי מלמעלה?')
        des2.vote( self.at1 ,  LikeLevel.BAD)
        des2.vote( self.at2 ,  LikeLevel.MEDIUM)
        des2.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        d.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        d.add_feedback(self.at3, Feedback.ADVICE, "ADVICE this")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICE")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICEADVICE")
        
        
        des1 = d.add_decision( 'אולי מלמטה?')
        des1.vote( self.at1 ,  LikeLevel.EXCELLENT)
        des1.vote( self.at1 ,  LikeLevel.BAD)
        des1.vote( self.at2 ,  LikeLevel.MEDIUM)
        des1.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        des1.vote( self.at3 ,  LikeLevel.BAD)
        d.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        task2 = d.add_task(self.at2, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        task3= d.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        task2.close(self.admin)
        des2 = d.add_decision( 'אולי מלמעלה?')
        des2.vote( self.at1 ,  LikeLevel.BAD)
        des2.vote( self.at2 ,  LikeLevel.MEDIUM)
        des2.vote( self.at2 ,  LikeLevel.VERY_GOOD)        

        d2 = self.create_dicussion()
        d2.add_feedback(self.at3, Feedback.COOPERATION, "COOPERATION this")
        d2.add_feedback(self.at3, Feedback.COOPERATION, "like COOPERATION")
        d2.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        d.add_feedback(self.at3, Feedback.ADVICE, "ADVICE this")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICE")
        d.add_feedback(self.at1, Feedback.ADVICE, "like ADVICEADVICE")
        
        
        des1 = d.add_decision( 'אולי מלמטה?')
        des1.vote( self.at1 ,  LikeLevel.EXCELLENT)
        des1.vote( self.at1 ,  LikeLevel.BAD)
        des1.vote( self.at2 ,  LikeLevel.MEDIUM)
        des1.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        des3.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        des3.vote( self.at3 ,  LikeLevel.BAD)
        d2.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        d2.add_feedback(self.at1, Feedback.INTUITION, "like INTUITION")
        task4 = d.add_task(self.at2, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        task5= d.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        task5.close(self.at2)
        des2 = d2.add_decision( 'אולי מלמעלה?')
        des2.vote( self.at1 ,  LikeLevel.BAD)
        des2.vote( self.at2 ,  LikeLevel.MEDIUM)
        des2.vote( self.at2 ,  LikeLevel.VERY_GOOD)        
        d.add_feedback(self.at2, Feedback.INTUITION, "INTUITION this")
        task2 = d2.add_task(self.at2, 'd2 1s1', timezone.now() +  datetime.timedelta(seconds =2))
        task3= d2.add_task(self.admin, 'd2 2nd', timezone.now() +  datetime.timedelta(seconds =2))
        
        print 'before delete'
        print 'discuddions', Discussion.objects.count() 
        print 'feedbacks', Feedback.objects.count() 
        print 'Decision', Decision.objects.count() 
        print 'Vote', Vote.objects.count() 
        print 'Task', Task.objects.count() 
        Feedback, Decision, LikeLevel, Vote, Task
        d.print_content()
        d2.print_content()
        d2.delete()
        print 'after delete'
        print 'discuddions', Discussion.objects.count() 
        print 'feedbacks', Feedback.objects.count() 
        print 'Decision', Decision.objects.count() 
        print 'Vote', Vote.objects.count() 
        print 'Task', Task.objects.count() 
        d.print_content()
        self.assertEquals(2, Discussion.objects.count())
        self.assertEquals(29, Feedback.objects.count())
        self.assertEquals(7, Decision.objects.count())
        self.assertEquals(17,  Vote.objects.count() )
        self.assertEquals(8, Task.objects.count())

    def test_discussion_iniactivation(self):
        
        """       
        I cannot test this feature as is since the time relolution of Discussion.is_active_and_time_to_inactivation()
                
        
        is days
        so i copied the same lines of code here for test with a seconds resolution.        
        """
        self.assertEquals(0, Task.objects.count())
        d = self.create_dicussion()
        task1 = d.add_task(self.at1, 'shall start', timezone.now() +  datetime.timedelta(seconds =4))
        task2 = d.add_task(self.at2, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        task3= d.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(3, Task.objects.count())
        time.sleep(1)
        task2.close(self.admin)
        time.sleep(2)
        task2.print_content()
        self.assertEquals(self.admin, task2.closed_by)
        self.assertEquals(False, task1.close(self.at1))
        self.assertEquals(task1.STARTED, task1.get_status())
        self.assertEquals(task1.CLOSED, task2.get_status())
        self.assertEquals(task1.MISSED, task3.get_status())
        
        print 'current tasks status------------------------------------'
        
        d.print_content()
        max_inactivity_seconds = 1
        d.locked_at = None
        d.save()        
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, False)
        
        max_inactivity_seconds = 5
        d.locked_at = None
        d.save()                
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, True)
        
        time.sleep(3)
        
        max_inactivity_seconds = 5
        d.locked_at = None
        d.save()                
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, False)
        time.sleep(1)
        
        max_inactivity_seconds = 5
        task3= d.add_task(self.admin, 'shall cause activation', timezone.now() +  datetime.timedelta(seconds =2), max_inactivity_seconds)
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, True)
        
        print 'discussion re-activation ---------------------------------'
        
        d = self.create_dicussion()

        max_inactivity_seconds = 5
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, True)
        time.sleep(2)
        max_inactivity_seconds = 5
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'after 2 sec max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, True)

        max_inactivity_seconds = 5
        task3= d.add_task(self.admin, '1st task', timezone.now() +  datetime.timedelta(seconds =2), max_inactivity_seconds)
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'after add a task max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, True)
        time.sleep(6)
        max_inactivity_seconds = 5
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'discussion should be locked task max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        
        self.assertEquals(active, False)
        
        max_inactivity_seconds = 5
        task3= d.add_task(self.admin, '2nd task', timezone.now() +  datetime.timedelta(seconds =2), max_inactivity_seconds)
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print 'discussion should be unlocked task max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left
        self.assertEquals(active, True)
        
    def test_attending_list(self):    
        dis = self.create_dicussion()
        dis.add_feedback(self.at1, Feedback.ENCOURAGE, "like this")
        
        
        decision = dis.add_decision( 'אולי מלמטה?')
        decision.vote( self.at2 ,  LikeLevel.EXCELLENT)
        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 2)       
        task2 = dis.add_task(self.at3, 'shall close', timezone.now() +  datetime.timedelta(seconds =2))
        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 3)       
        attending_list = dis.get_attending_list(True)
        self.assertEquals(len(attending_list), 4)       
        task3= dis.add_task(self.admin, 'shall missed', timezone.now() +  datetime.timedelta(seconds =2))
        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 3)       
        
    def test_viewers(self):
        d = self.create_dicussion()
        self.assertEquals(d.viewer_set.count(), 0) 
        d.record_a_view(self.at1) 
        d.save()     
        d.record_a_view(self.at2) 
        d.save()     
        d.record_a_view(self.at3) 
        d.save()     
        d.record_a_view(self.at1) 
        d.save()     
        d.record_a_view(self.at2) 
        d.save()     
        d.record_a_view(self.at2) 
        d.save()     
        d.record_a_view(self.at2) 
        d.save()
        at1_view = d.viewer_set.get( user = self.at1)
        at2_view = d.viewer_set.get( user = self.at2)
        at3_view = d.viewer_set.get( user = self.at3)
             
        self.assertEquals(at1_view.views_counter, 2) 
        self.assertEquals(at2_view.views_counter, 4) 
        self.assertEquals(at3_view.views_counter, 1) 
        self.assertEquals(d.viewer_set.count(), 3) 
        print "viewers test"
        d.print_content()
        print "viewers test print end"

        
    def test_discussion_followers(self):
        d = self.create_dicussion()
        self.assertEquals(d.is_a_follower( self.at1), False) 
        self.assertEquals(d.viewer_set.count(), 0) 
        
        d.start_follow( self.at1)
        self.assertEquals(d.is_a_follower( self.at1), True) 
        self.assertEquals(d.viewer_set.count(), 1) 
        
        d.stop_follow( self.at1)
        self.assertEquals(d.is_a_follower( self.at1), False) 
        self.assertEquals(d.viewer_set.count(), 1) 
        
        d.start_follow( self.at2)
        self.assertEquals(d.is_a_follower( self.at2), True) 
        self.assertEquals(d.viewer_set.count(), 2) 
        
        followers_list = d.get_followers_list()
        self.assertEquals( self.at3 in followers_list , False)
         
        d.start_follow( self.at3)
        
        followers_list = d.get_followers_list()
        self.assertEquals( self.at3 in followers_list , True) 
        
        self.assertEquals( len(followers_list) , 2) 
        self.assertEquals(d.viewer_set.count(), 3) 
        
        d.start_follow( self.at1)
        followers_list = d.get_followers_list()
        self.assertEquals( len(followers_list), 3)
        
        print "followers test"
        d.print_content()
        print "followers test print end"

    def test_following_user(self):
        
        self.assertEquals(FollowRelation.objects.count(), 0) 
        self.assertEquals(is_user_is_following(self.at1, self.at2), False)
        self.assertEquals(is_user_is_following(self.at2, self.at1), False)
        start_users_following(self.at1, self.at2)
        self.assertEquals(is_user_is_following(self.at1, self.at2), True)         
        self.assertEquals(is_user_is_following(self.at2, self.at1), False)

        stop_users_following(self.at1, self.at2)
        
        self.assertEquals(is_user_is_following(self.at1, self.at2), False)
        self.assertEquals(is_user_is_following(self.at2, self.at1), False)

        start_users_following(self.at1, self.at3)
        
        start_users_following(self.at1, self.admin)

        start_users_following(self.at3, self.at1)
        
        self.assertEquals(is_user_is_following(self.at1, self.at3), True)
        self.assertEquals(is_user_is_following(self.at3, self.at1), True)
        self.assertEquals(is_user_is_following(self.at1, self.admin), True)
        
        start_users_following(self.at3, self.at1)
        start_users_following(self.at3, self.at2)
        start_users_following(self.at3, self.at3)

        self.assertEquals(FollowRelation.objects.count(), 4) 
        
        print FollowRelation.objects.all()

        
        self.assertEquals(is_user_is_following(self.at3, self.at1), True)
        self.assertEquals(is_user_is_following(self.at3, self.at2), True)
        self.assertEquals(is_user_is_following(self.at3, self.at3), False)
        
        at1_followers_list = get_followers_list(self.at1)
        print 'at1_followers_list',  at1_followers_list
        self.assertEquals( self.at1 in at1_followers_list, False)
        self.assertEquals( self.at2 in at1_followers_list, False)
        self.assertEquals( self.at3 in at1_followers_list, True)
        self.assertEquals( self.admin in at1_followers_list, False)
        

        at1_following_list = get_following_list(self.at1)
        print 'at1_following_list', at1_following_list
        self.assertEquals( self.at1 in at1_following_list, False)
        self.assertEquals( self.at2 in at1_following_list, False)
        self.assertEquals( self.at3 in at1_following_list, True)
        self.assertEquals( self.admin in at1_following_list, True)

    def test_discussion_invitations(self):
        d = self.create_dicussion()
        self.assertEquals(d.viewer_set.count(), 0) 
        self.assertEquals(d.can_user_participate( self.at1), True)
        d.is_restricted = True
        d.save()
        self.assertEquals(d.can_user_participate( self.at1), False)
        self.assertEquals(d.viewer_set.count(), 0) 

        
        d.invite( self.at1)
        self.assertEquals(d.can_user_participate( self.at1), True) 
        self.assertEquals(d.viewer_set.count(), 1) 
        
        d.cancel_invitation( self.at1)
        self.assertEquals(d.is_user_invited( self.at1), False) 
        self.assertEquals(d.can_user_participate( self.at1), False)
        self.assertEquals(d.viewer_set.count(), 1) 
        
        d.invite( self.at2)
        self.assertEquals(d.is_user_invited( self.at2), True) 
        self.assertEquals(d.viewer_set.count(), 2) 
        
        followers_list = d.get_followers_list()
        self.assertEquals( self.at3 in followers_list , False)
         
        d.invite( self.at3)
        
        invited_users_list  = d.get_invited_users_list()
        self.assertEquals( self.at3 in invited_users_list , True) 
        
        self.assertEquals( len(invited_users_list) , 2) 
        self.assertEquals(d.viewer_set.count(), 3) 
        
        d.invite( self.at1)
        invited_users_list = d.get_invited_users_list()
        self.assertEquals( len(invited_users_list), 3)
        
        print 'invited_users_list', invited_users_list
        d.cancel_invitation( self.at2)
        d.print_content()
        
    def test_segments(self):
        print 'test_segments start'

        self.assertEquals(Segment.objects.count(), 0) 
        
        seg1 = Segment( title ='seg1')
        seg1.save()
        seg2 = Segment( title ='seg2')
        seg2.save()
        self.assertEquals(Segment.objects.count(), 2) 
        
        self.assertEquals( self.admin.userprofile.is_in_the_same_segment( self.at1), True)
        self.admin.userprofile.set_segment()
        self.assertEquals( self.admin.userprofile.is_in_the_same_segment( self.at1), True)
        print seg1
        self.admin.userprofile.set_segment( seg1)

        self.at1.userprofile.print_content()
        self.admin.userprofile.print_content()
        
        self.assertEquals( self.admin.userprofile.is_in_the_same_segment( self.at1), False)
        
        self.at1.userprofile.set_segment( seg1)
        self.assertEquals( self.admin.userprofile.is_in_the_same_segment( self.at1), True)
        
        self.at2.userprofile.set_segment( seg1)
        self.assertEquals( self.admin.userprofile.is_in_the_same_segment( self.at2), True)
        
        self.at2.userprofile.set_segment( seg2)
        self.assertEquals( self.admin.userprofile.is_in_the_same_segment( self.at2), False)

        self.assertEquals( self.at3.userprofile.is_in_the_same_segment( self.at2), False)
        
        self.at3.userprofile.set_segment( seg2)
        
        self.assertEquals( self.at3.userprofile.is_in_the_same_segment( self.at2), True)
        
        admin_all_users_in_same_segment_list = self.admin.userprofile.get_all_users_in_same_segment_list()
        for user in admin_all_users_in_same_segment_list:
            print user.userprofile.print_content
        
        at1_all_users_in_same_segment_list = self.at1.userprofile.get_all_users_in_same_segment_list()
        at2_all_users_in_same_segment_list = self.at2.userprofile.get_all_users_in_same_segment_list()
        at4_all_users_in_same_segment_list = self.at4.userprofile.get_all_users_in_same_segment_list()
        
        self.assertEquals( self.at1 in admin_all_users_in_same_segment_list, True)        
        self.assertEquals( self.at2 in admin_all_users_in_same_segment_list, False)        
        self.assertEquals( self.admin in at1_all_users_in_same_segment_list, True)        
        self.assertEquals( self.at1 in at1_all_users_in_same_segment_list, False)        
        self.assertEquals( self.at2 in at1_all_users_in_same_segment_list, False)        
        self.assertEquals( self.at3 in at1_all_users_in_same_segment_list, False)        
        self.assertEquals( self.at4 in at1_all_users_in_same_segment_list, False)        
        
        self.assertEquals( len(admin_all_users_in_same_segment_list), 1)        
        self.assertEquals( len(at2_all_users_in_same_segment_list), 1)        
        self.assertEquals( len(at4_all_users_in_same_segment_list), 2)
                
        d = self.create_dicussion()
        
        self.assertEquals(d.is_user_in_discussion_segment( self.admin), True) 
        self.assertEquals(d.is_user_in_discussion_segment( self.at1), True) 
        self.assertEquals(d.is_user_in_discussion_segment( self.at2), False) 
        self.assertEquals(d.is_user_in_discussion_segment( self.at4), False) 

    def test_user_update(self):
        print 'test_user_update start'
        self.assertEquals(UserUpdate.objects.count(), 0)
        d = self.create_dicussion()
         
        post_update_to_user(self.at1.id, header = 'כותרת', content = 'תוכן', discussion_id = d.id, sender_user_id = self.at2.id,  details_url = 'www.hp.com')
        
        post_update_to_user(self.at1.id, header = '3כותרת', content = '3תוכן', discussion_id = d.id, sender_user_id = self.at3.id,  details_url = 'www.hp.com')

        post_update_to_user(self.at2.id, header = '4כותרת', content = '4תוכן', discussion_id = d.id, sender_user_id = self.at3.id,  details_url = 'www.hp.com')
        
        self.assertEquals(UserUpdate.objects.count(), 3)
        for user_update in UserUpdate.objects.all():
            user_update.print_content()
        
        
    def test_user_glimpse_a_discussion(self):
        print 'test_user_glimpse_a_discussion'
        d = self.create_dicussion()
        self.assertEquals(d.viewer_set.count(), 0) 
        d.record_a_view(self.at1)#no following save - counters shall not incremented     
        
        at1_view = d.viewer_set.get( user = self.at1)
        self.assertEquals(d.viewer_set.count(), 1) 
        self.assertEquals(at1_view.glimpse_set.count(), 1) 
        d.record_a_view(self.at1)        
        at1_view = d.viewer_set.get( user = self.at1)
        self.assertEquals(at1_view.glimpse_set.count(), 1)
        self.assertEquals(at1_view.get_views_counter(), 1)
        d.save() 
        d.record_a_view(self.at1)        
        at1_view = d.viewer_set.get( user = self.at1)
        self.assertEquals(at1_view.glimpse_set.count(), 2)
        self.assertEquals(at1_view.get_views_counter(), 2)        

        d.save() 
        d.record_a_view(self.at2)        
        d.save() 
        d.record_a_view(self.at3)        
        d.save() 
        d.record_a_view(self.at1)
        self.assertEquals(Glimpse.objects.count(), 5)
        for glimpse in Glimpse.objects.all().order_by("-created_at"):
            glimpse.print_content()

       
                
        
        

    def test_rewards(self):    
        print 'test_rewards'
        d = self.create_dicussion()
        d.add_feedback(self.at1, Feedback.ENCOURAGE, "like this")
        
        
        des1 = d.add_decision( 'אולי מלמטה?')
        des1.vote( self.at1 ,  LikeLevel.EXCELLENT)
        task2 = d.add_task(self.at1, 'shall close', timezone.now() +  datetime.timedelta(seconds =1))
        task2.close(self.admin)
        task4 = d.add_task(self.admin, 'shall close', timezone.now() +  datetime.timedelta(seconds =1))
        task4.close(self.at1)
        
        task5 = d.add_task(self.at1, 'shall abort', timezone.now() +  datetime.timedelta(seconds =1))
        task5.abort(self.admin)
        task6 = d.add_task(self.admin, 'shall shall abort', timezone.now() +  datetime.timedelta(seconds =1))
        task6.abort(self.at1)
        
        time.sleep(3)        
        
        d.record_a_view(self.at1)
        d.print_content()
        self.admin.account = Account.objects.get(id = self.admin.account.id)
        self.at1.account = Account.objects.get(id = self.at1.account.id)
        self.admin.account.print_content()
        self.at1.account.print_content()        
        
        self.assertEquals(84,  self.admin.account.get_credit())
        self.assertEquals(76,  self.at1.account.get_credit())
