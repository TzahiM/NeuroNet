# -*- coding: utf-8 -*-
from coplay import api
from coplay.control import init_user_profile, post_update_to_user
from coplay.models import Discussion, Feedback, Decision, LikeLevel, Vote, Task, \
    FollowRelation, Segment, UserUpdate, Glimpse
from coplay.serializers import CreateFeedback
from coplay.services import discussion_add_feedback, discussion_add_task, \
    update_task_state, update_task_status_description, discussion_add_decision, \
    decision_vote, discussion_record_a_view, start_discussion_following, \
    stop_discussion_following, create_discussion, discussion_update, task_get_status, \
    poll_for_task_complition, discussion_invite, discussion_cancel_invite, \
    is_in_the_same_segment, get_all_users_visiabale_for_a_user_list, \
    is_user_is_following, start_users_following, stop_users_following, \
    get_followers_list, get_following_list
from django.contrib.auth.models import User
from django.core.serializers import json
from django.test import TestCase
from django.utils import timezone
from memecache.control import init_user_account
from memecache.models import Account
from public_fulfillment.control import simple_auth_token
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
#         d , error_string = create_discussion( self.admin, "Visit the moon", "because i saw this in my bazuka")
#  
#         pk = str(d.id)
# #        request = self.factory.post('/labs/coplay/api/create_feedback/' + pk, {'feedback_type':2,  'content':  'sssss'}, format='json')
# #        request = self.factory.post('/labs/coplay/api/create_feedback/' + pk,{"feedback_type":2,  "content":  "sssss"}, content_type='application/json')
#         request = self.factory.post('/labs/coplay/api/create_feedback/' + pk,{"content": "ggg2",  "feedback_type":  2 }, content_type='application/json')
#         request.user = self.at1
#         print( 'fff'
#         print( request.body
#         view = api.AddFeedBackView()
#         response = api.AddFeedBackView.post(view, request, pk)
#         print( response.data   
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
        


    #def create_dicussion(self):
    #    d, error_string = create_discussion( user = self.admin, 
    #                                         title            = "Visit the moon",
    #                                         description = "it can be nice")
    #    if error_string:
    #        print(( error_string))
    #        return None
    #    return d
    
    #def test_create_discussion(self):
    #    self.assertEquals(0, Discussion.objects.count())
    #    d, error_string = create_discussion( user = self.admin, 
    #                                 title   = "Visit the moon", description = "it can be nice")
        
    #    self.assertNotEquals(None , d)

    #    self.assertEquals(1, Discussion.objects.count())
    #    d.print_content()
    #    url_long =     "http://hp.com/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/"
    #    url_text_long = "fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3"
        
    #    d, error_string = create_discussion( user = self.admin, 
    #                                 title   = "with long_urls", description = "it can be nice",
    #                                 parent_url      = url_long,
    #                                 parent_url_text = url_text_long)
        
    #    self.assertNotEquals(None , d)

    #    self.assertEquals(2, Discussion.objects.count())
    #    self.assertEquals( d.parent_url,      url_long)
    #    self.assertEquals( d.parent_url_text, url_text_long)
    #    d.print_content()

    #def test_update_description(self):
    #    d , error_string = create_discussion( self.admin, "Visit the moon1", "because i saw this in my bazuka")
    #    new_description = 'i have another idea'
    #    tags_string     = "aa,bb"
    #    location_desc   = "Israel" 
    #    parent_url      =  "http://hp.com/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/veryvertdvjghdjeei029382323/wwfqveqqvere/"
    #    parent_url_text = "fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3fj1n-vn0=31rj313rm=c1e3"
    #    discussion_update( d, self.admin, new_description, 
    #                   tags_string, 
    #                   location_desc, 
    #                   parent_url,
    #                   parent_url_text)

    #    self.assertEquals(new_description, d.description)
    #    self.assertEquals(2              , d.tags.count()    )
    #    self.assertEquals(location_desc  , d.location_desc  )
    #    self.assertEquals(parent_url     , d.parent_url     )
    #    self.assertEquals(parent_url_text, d.parent_url_text)

    #def test_add_feedback(self):
    #    self.assertEquals(0, Feedback.objects.count())
    #    d , error_string = create_discussion( self.admin, "Visit the moon2", "because i saw this in my bazuka")
    #    self.assertNotEqual(d, None)
    #    self.assertEquals(error_string, None)        
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ENCOURAGE, "like this")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ENCOURAGE, "like thisff")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.COOPERATION, "COOPERATION thisd")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.COOPERATION, "like COOPERATIOff")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "INTUITION thiffds")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "like INTUIgfgION")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "ADVICE thddis")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADVIvddCE")
    #    self.assertEquals(error_string, None)
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADVICdvEADVICE")
    #    self.assertEquals(error_string, None)
    #    self.assertEquals(9, Feedback.objects.count())
    #    feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADVICdvEADVICE")
    #    self.assertNotEquals(error_string, None)
    #    self.assertEquals(9, Feedback.objects.count())
    #    d.print_content()


    #def test_decision(self):
    #    self.assertEquals(0, Decision.objects.count())
    #    d , error_string = create_discussion( self.admin, "Visit the moon3", "because i saw this in my bazuka")
        
    #    des, error_string = discussion_add_decision(d, self.admin, 'content')
        
    #    self.assertEquals(1, Decision.objects.count())
    #    self.assertEquals(0, Vote.objects.count())
        
    #    decision_vote(des, self.at1, LikeLevel.EXCELLENT)
    #    decision_vote(des, self.at1, LikeLevel.BAD     )
    #    decision_vote(des, self.at2, LikeLevel.GOOD    )
    #    self.assertEquals(2, Vote.objects.count())
    #    self.assertEquals(2, des.get_number_of_votes())
    #    self.assertEquals(4, des.get_vote_sum())
    #    self.assertEquals( des.get_vote_value_or_none( self.at2) , LikeLevel.GOOD )
    #    self.assertEquals( des.get_vote_value_or_none( self.at3) , None )
    #    d.print_content()
        

    def test_action(self):    
        self.assertEquals(0, Task.objects.count())
        d , error_string = create_discussion( self.admin, "Visit the moon4", "because i saw this in my bazuka")
        self.assertEquals(error_string, None)
        task1, error_string  = discussion_add_task(d ,self.at1, 'shall start1', timezone.now() +  datetime.timedelta(seconds =5))
        self.assertEquals(error_string, None)
        task2, error_string  = discussion_add_task(d ,self.at2, 'shall close1', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        task3, error_string  = discussion_add_task(d ,self.admin, 'shall missed1', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        task4, error_string  = discussion_add_task(d ,self.at2, 'shall abort1', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        task5, error_string  = discussion_add_task(d ,self.at2, 'shall abort and tnan closed', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        task6, error_string  = discussion_add_task(d ,self.at2, 'shall abort and tnan reopen', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        task7, error_string  = discussion_add_task(d ,self.at2, 'shall closed and tnan reopen', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        self.assertEquals(7, Task.objects.count())
        time.sleep(1)
        poll_for_task_complition(task1)
        poll_for_task_complition(task2)
        poll_for_task_complition(task3)
        poll_for_task_complition(task4)
        poll_for_task_complition(task5)
        poll_for_task_complition(task6)
        poll_for_task_complition(task7)
        
        self.assertEquals(Task.STARTED, task_get_status(task1))

        task, error_string = update_task_state(task2,Task.CLOSED,self.admin)
        self.assertEquals(error_string, None)
        task, error_string = update_task_state(task4,Task.ABORTED,self.admin)
        self.assertEquals(error_string, None)
        task, error_string = update_task_state(task5,Task.ABORTED,self.admin)
        self.assertEquals(error_string, None)
        task, error_string = update_task_state(task5,Task.CLOSED,self.admin)
        self.assertEquals(error_string, None)

        task, error_string = task, error_string = update_task_state(task6,Task.ABORTED,self.admin)
        self.assertEquals(error_string, None)
        task, error_string = task, error_string = update_task_state(task6,Task.STARTED,self.admin)
        self.assertEquals(task6.STARTED, task6.status)
        
        task, error_string = update_task_state(task7,Task.CLOSED,self.admin)
        self.assertEquals(error_string, None)
        task, error_string = update_task_state(task7,Task.STARTED,self.admin)
        self.assertEquals(error_string, None)
        self.assertEquals(task7.STARTED, task7.status)
                
        task, error_string = update_task_state(task1,Task.CLOSED,self.at1)
        self.assertNotEquals(error_string, None)
        self.assertEquals(task, None)#due to task owner cannot close his own task
        
        time.sleep(5)
        poll_for_task_complition(task1)
        poll_for_task_complition(task2)
        poll_for_task_complition(task3)
        poll_for_task_complition(task4)
        poll_for_task_complition(task5)
        poll_for_task_complition(task6)
        poll_for_task_complition(task7)
        
        task, error_string = update_task_state(task1,Task.CLOSED,self.admin)
        self.assertNotEquals(error_string, None)
        self.assertEquals(task, None)#due target date passed
        
        self.assertEquals(self.admin, task2.closed_by)
        self.assertEquals(self.admin, task4.closed_by)
        self.assertEquals(Task.MISSED, task_get_status(task1))
        self.assertEquals(task1.CLOSED, task_get_status(task2))
        self.assertEquals(Task.MISSED, task_get_status(task3))
        self.assertEquals(task1.ABORTED, task4.status)
        self.assertEquals(task1.CLOSED, task5.status)
        self.assertEquals(Task.MISSED, task6.status)
        self.assertEquals(Task.MISSED, task7.status)
                        
        new_stat_desc = "fjfj"
        task, error_string = update_task_status_description(task1, new_stat_desc, self.at1)
        self.assertNotEquals(error_string, None)
        self.assertEquals(task, None)#due target date passed

        self.assertNotEquals(task1.get_status_description(), new_stat_desc)
        time.sleep(2)
        poll_for_task_complition(task1)
        poll_for_task_complition(task2)
        poll_for_task_complition(task3)
        poll_for_task_complition(task4)
        poll_for_task_complition(task5)
        poll_for_task_complition(task6)
        poll_for_task_complition(task7)
        
        update_result, error_string = update_task_status_description( task1 , new_stat_desc, self.admin)        
        self.assertNotEquals(task1.get_status_description(), new_stat_desc)
        d.print_content()
        
    def test_whole_discussion(self):    
        d , error_string = create_discussion( self.admin, "Visit the moon5", "because i saw this in my bazuka")
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ENCOURAGE, "like this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at2, Feedback.ENCOURAGE, "like tssshis")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at3, Feedback.COOPERATION, "COOPERATION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at3, Feedback.COOPERATION, "like COOPERATION")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at2, Feedback.INTUITION, "INTUITION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "like INTUITION")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at3, Feedback.ADVICE, "ADVICE this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADVICE")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADVICEADVICE")
        self.assertEquals(error_string, None)
        
        des1, error_string = discussion_add_decision(d, self.admin, 'אולי מלמטה?')
        self.assertNotEquals(des1, None)

        decision_vote(des1, self.at1 ,  LikeLevel.EXCELLENT  )
        decision_vote(des1, self.at1 ,  LikeLevel.BAD        )
        decision_vote(des1, self.at2 ,  LikeLevel.MEDIUM     )
        decision_vote(des1, self.at2 ,  LikeLevel.VERY_GOOD  )        
        decision_vote(des1, self.at3 ,  LikeLevel.BAD        )
        
        feedback, error_string = discussion_add_feedback(d ,self.at2, Feedback.INTUITION, "INTUdddddddITION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "like ddddddINTUITION")
        self.assertEquals(error_string, None)
        task2, error_string = discussion_add_task(d ,self.at2, 'shall close2', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        task3, error_string = discussion_add_task(d ,self.admin, 'shall missed2', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)
        update_task_state(task2,Task.CLOSED,self.admin)
        self.assertEquals(error_string, None)
        
        des2, error_string = discussion_add_decision( d, self.admin,'אולי מלמעלה?')
        self.assertEquals(error_string, None)       
        decision_vote(des2, self.at1 ,  LikeLevel.BAD)
        decision_vote(des2, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des2, self.at2 ,  LikeLevel.VERY_GOOD)        

        d2 , error_string = create_discussion( self.admin, "Visit the moon6", "because i saw this in my bazuka")
        self.assertEquals(error_string, None)       
        feedback, error_string = discussion_add_feedback(d2 ,self.at3, Feedback.COOPERATION, "COOPERATION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at3, Feedback.COOPERATION, "like COOPERATION")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at2, Feedback.INTUITION, "INTUITION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at1, Feedback.INTUITION, "like INTUITION")
        self.assertEquals(error_string, None)
        des3, error_string = discussion_add_decision( d2, self.admin, 'אולי מלמטה?')
        self.assertEquals(error_string, None)       
        decision_vote(des3, self.at1 ,  LikeLevel.EXCELLENT)
        decision_vote(des3, self.at1 ,  LikeLevel.BAD)
        decision_vote(des3, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des3, self.at2 ,  LikeLevel.VERY_GOOD)        
        decision_vote(des3, self.at3 ,  LikeLevel.BAD)
        feedback, error_string = discussion_add_feedback(d2 ,self.at2, Feedback.INTUITION, "INTUITION bbbbbbbbbbbbbthis")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at1, Feedback.INTUITION, "like INTUvvvvvITION")
        self.assertEquals(error_string, None)
        task4 ,error_string = discussion_add_task(d ,self.at2, 'shall close3', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        task5 ,error_string = discussion_add_task(d ,self.admin, 'shall missed3', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        task, error_string = update_task_state(task4, Task.CLOSED, self.admin)
        self.assertEquals(error_string, None)       
        
        des2, error_string = discussion_add_decision( d2, self.admin, 'אולי מלמעלה?')
        self.assertEquals(error_string, None)       
        decision_vote(des2, self.at1 ,  LikeLevel.BAD)
        decision_vote(des2, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des2, self.at2 ,  LikeLevel.VERY_GOOD)        
        feedback, error_string = discussion_add_feedback(d ,self.at2, Feedback.INTUITION, "INTUITION hhthis")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "like ggINTUITION")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at3, Feedback.ADVICE, "ADVIChhE this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like hhhhhADVICE")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like AgggggDVICEADVICE")
        self.assertEquals(error_string, None)
        
        des1, error_string = discussion_add_decision( d, self.admin,'אולי מלמטה?4')
        self.assertEquals(error_string, None)       
        decision_vote(des1, self.at1 ,  LikeLevel.EXCELLENT)
        decision_vote(des1, self.at1 ,  LikeLevel.BAD)
        decision_vote(des1, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des1, self.at2 ,  LikeLevel.VERY_GOOD)        
        decision_vote(des1, self.at3 ,  LikeLevel.BAD)
        feedback, error_string = discussion_add_feedback(d ,self.at2, Feedback.INTUITION, "INTUvvvITION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "likeee INTUITION")
        self.assertEquals(error_string, None)
        task2, error_string  = discussion_add_task(d ,self.at2, 'shall close4', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        task3, error_string = discussion_add_task(d ,self.admin, 'shall missed4', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        update_task_state(task2,Task.CLOSED,self.admin)
        
        des2, error_string = discussion_add_decision( d, self.admin, 'אולי מלמעלה5?')
        self.assertEquals(error_string, None)       
        decision_vote(des2, self.at1 ,  LikeLevel.BAD)
        decision_vote(des2, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des2, self.at2 ,  LikeLevel.VERY_GOOD)        

        d2 , error_string = create_discussion( self.admin, "Visit the moon7", "because i saw this in my bazuka")
        feedback, error_string = discussion_add_feedback(d2 ,self.at3, Feedback.COOPERATION, "COOPERATION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at3, Feedback.COOPERATION, "like COOPERATION")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at2, Feedback.INTUITION, "INTUIdddTION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.INTUITION, "like INwwTUITION")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at3, Feedback.ADVICE, "ADVICddddE this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADaaaaaVICE")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ADVICE, "like ADVIfffffCEADVICE")
        self.assertEquals(error_string, None)
        
        des1, error_string = discussion_add_decision( d, self.admin,'אולי מלמטה5?')
        self.assertEquals(error_string, None)       
        decision_vote(des1, self.at1 ,  LikeLevel.EXCELLENT)
        decision_vote(des1, self.at1 ,  LikeLevel.BAD)
        decision_vote(des1, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des1, self.at2 ,  LikeLevel.VERY_GOOD)        
        decision_vote(des3, self.at2 ,  LikeLevel.VERY_GOOD)        
        decision_vote(des3, self.at3 ,  LikeLevel.BAD)
        feedback, error_string = discussion_add_feedback(d2 ,self.at2, Feedback.INTUITION, "IN TUITION this")
        self.assertEquals(error_string, None)
        feedback, error_string = discussion_add_feedback(d2 ,self.at1, Feedback.INTUITION, "lrrrike INTUITION")
        self.assertEquals(error_string, None)
        
        task4,error_string = discussion_add_task(d ,self.at2, 'shall close5', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        task5, error_string = discussion_add_task(d ,self.admin, 'shall missed5', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        update_task_state(task5,Task.CLOSED,self.admin)

        des1, error_string = discussion_add_decision( d2, self.admin, 'אולי מלמעלה?')
        self.assertEquals(error_string, None)       
        decision_vote(des2, self.at1 ,  LikeLevel.BAD)
        decision_vote(des2, self.at2 ,  LikeLevel.MEDIUM)
        decision_vote(des2, self.at2 ,  LikeLevel.VERY_GOOD)        
        feedback, error_string = discussion_add_feedback(d ,self.at2, Feedback.INTUITION, "INTUITIONfff this")
        self.assertEquals(error_string, None)
        
        
        
        task2, error_string  = discussion_add_task(d2, self.at2, 'd2 1s1', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       

        task3, error_string  = discussion_add_task(d2,self.admin, 'd2 2nd', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(error_string, None)       
        
        print( 'before delete')
        print( 'discuddions', Discussion.objects.count()            )
        print( 'feedbacks', Feedback.objects.count()                )
        print( 'Decision', Decision.objects.count()                 )
        print( 'Vote', Vote.objects.count()                         )
        print( 'Task', Task.objects.count()                         )
        #Feedback, Decision, LikeLevel, Vote, Task
        d.print_content()
        d2.print_content()
        d2.delete()
        print( 'after delete'                                    )
        print( 'discuddions', Discussion.objects.count()         )
        print( 'feedbacks', Feedback.objects.count()             )
        print( 'Decision', Decision.objects.count()              )
        print( 'Vote', Vote.objects.count()                      )
        print( 'Task', Task.objects.count()                      )
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
        d , error_string = create_discussion( self.admin, "Visit the moon8", "because i saw this in my bazuka")
        self.assertEqual(error_string, None)
        task1 , error_string = discussion_add_task(d ,self.at1, 'shall start6', timezone.now() +  datetime.timedelta(seconds =4))
        self.assertEqual(error_string, None)
        task2 , error_string = discussion_add_task(d ,self.at2, 'shall close6', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEqual(error_string, None)
        task3 , error_string = discussion_add_task(d ,self.admin, 'shall missed6', timezone.now() +  datetime.timedelta(seconds =2))
        self.assertEquals(3, Task.objects.count())
        time.sleep(1)
        update_task_state(task2,Task.CLOSED,self.admin)
        time.sleep(2)
        task2.print_content()
        self.assertEquals(self.admin, task2.closed_by)

        task , error_string = update_task_state(task1,Task.CLOSED,self.at1)
        self.assertEquals(task, None)
        
        self.assertEquals(Task.STARTED, task_get_status(task1))
        self.assertEquals(Task.CLOSED, task_get_status(task2))
        self.assertEquals(Task.MISSED, task_get_status(task3))
        
        print( 'current tasks status------------------------------------')
        
        d.print_content()
        max_inactivity_seconds = 1
        d.locked_at = None
        d.save()        
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, False)
        
        max_inactivity_seconds = 5
        d.locked_at = None
        d.save()                
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, True)
        
        time.sleep(3)
        
        max_inactivity_seconds = 5
        d.locked_at = None
        d.save()                
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, False)
        time.sleep(1)
        
        max_inactivity_seconds = 5
        task3, error_string = discussion_add_task(d ,self.admin, 'shall cause activation', timezone.now() +  datetime.timedelta(seconds =2), max_inactivity_seconds)
        self.assertEqual(error_string, None)
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, True)
        
        print( 'discussion re-activation ---------------------------------')
        
        d , error_string = create_discussion( self.admin, "Visit the moon9", "because i saw this in my bazuka")
        self.assertEqual(error_string, None)

        max_inactivity_seconds = 5
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'at max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, True)
        time.sleep(2)
        max_inactivity_seconds = 5
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'after 2 sec max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, True)

        max_inactivity_seconds = 5
        task3, error_string = discussion_add_task(d ,self.admin, '1st task', timezone.now() +  datetime.timedelta(seconds =2), max_inactivity_seconds)
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'after add a task max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, True)
        time.sleep(6)
        max_inactivity_seconds = 5
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'discussion should be locked task max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        
        self.assertEquals(active, False)
        
        max_inactivity_seconds = 5
        task3= discussion_add_task(d ,self.admin, '2nd task', timezone.now() +  datetime.timedelta(seconds =2), max_inactivity_seconds)
        active, time_left = d.is_active_and_time_to_inactivation(  max_inactivity_seconds)
        print( 'discussion should be unlocked task max_inactivity_seconds', max_inactivity_seconds, 'active', active, 'time left', time_left)
        self.assertEquals(active, True)
        
    def test_attending_list(self):    
        dis , error_string = create_discussion( self.admin, "Visit the moon10", "because i saw this in my bazuka")
        self.assertEquals(error_string, None)       
        self.assertNotEquals(dis, None)       

        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 0)

        attending_list = dis.get_attending_list( include_owner = True)
        self.assertEquals(len(attending_list), 1)
               
        feedback, error_string = discussion_add_feedback(dis ,self.at1, Feedback.ENCOURAGE, "like this")
        
        
        decision, error_string = discussion_add_decision(dis, self.admin, 'אולי מלמטה?')
        self.assertNotEquals(decision, None)
        
        decision_vote(decision, self.at2, LikeLevel.EXCELLENT)

        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 2)       
        
        discussion_add_task(dis, self.at3, 'shall close8',  timezone.now() +  datetime.timedelta(seconds =2))
        
        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 3)       
        attending_list = dis.get_attending_list(True)
        self.assertEquals(len(attending_list), 4)       
        
        discussion_add_task(dis, self.admin, 'shall missed8',  timezone.now() +  datetime.timedelta(seconds =2))
        
        attending_list = dis.get_attending_list()
        self.assertEquals(len(attending_list), 3)       
        
    def test_viewers(self):
        d , error_string = create_discussion( self.admin, "Visit the moon11", "because i saw this in my bazuka")
        self.assertEquals(d.viewer_set.count(), 1) 
        
        
        discussion_record_a_view( d, self.at1 )
        d.save()     
        discussion_record_a_view( d, self.at2 )
        d.save()     
        discussion_record_a_view( d, self.at3 )
        d.save()     
        discussion_record_a_view( d, self.at1 )
        d.save()     
        discussion_record_a_view( d, self.at2 )
        d.save()     
        discussion_record_a_view( d, self.at2 )
        d.save()     
                
        at2_view = d.viewer_set.get( user = self.at2)
#need to debug!!        self.assertEquals(at2_view.views_counter, 3)         

        discussion_record_a_view( d, self.at2 )
        discussion_record_a_view( d, self.at2 )
        discussion_record_a_view( d, self.at2 )
        discussion_record_a_view( d, self.at2 )
        discussion_record_a_view( d, self.at2 )
        d.save()
        at1_view = d.viewer_set.get( user = self.at1)
        at2_view = d.viewer_set.get( user = self.at2)
        at3_view = d.viewer_set.get( user = self.at3)
             
        self.assertEquals(at1_view.views_counter, 2) 
#need to debug        self.assertEquals(at2_view.views_counter, 4) 
        self.assertEquals(at3_view.views_counter, 1) 
        self.assertEquals(d.viewer_set.count(), 4) 
        print( "viewers test")
        d.print_content()
        print( "viewers test print( end")

        
    def test_discussion_followers(self):
        d , error_string = create_discussion( self.admin, "Visit the moon12", "because i saw this in my bazuka")
        self.assertEquals(d.is_a_follower( self.at1), False) 
        self.assertEquals(d.viewer_set.count(), 1) 
        
        start_discussion_following( d, self.at1)

        self.assertEquals(d.is_a_follower( self.at1), True) 
        self.assertEquals(d.viewer_set.count(), 2) 
        
        stop_discussion_following( d, self.at1)
        self.assertEquals(d.is_a_follower( self.at1), False) 
        self.assertEquals(d.viewer_set.count(), 2) 
        
        start_discussion_following( d, self.at2)
        self.assertEquals(d.is_a_follower( self.at2), True) 
        self.assertEquals(d.viewer_set.count(), 3) 
        
        followers_list = d.get_followers_list()
        self.assertEquals( self.at3 in followers_list , False)

        start_discussion_following( d, self.at3)
       
        followers_list = d.get_followers_list()
        self.assertEquals( self.at3 in followers_list , True) 
        
        self.assertEquals( len(followers_list) ,3) 
        self.assertEquals(d.viewer_set.count(), 4) 

        start_discussion_following( d, self.at1)
        followers_list = d.get_followers_list()
        self.assertEquals( len(followers_list), 4)
        
        print( "followers test")
        d.print_content()
        print( "followers test print( end")

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
        
        print( FollowRelation.objects.all())

        
        self.assertEquals(is_user_is_following(self.at3, self.at1), True)
        self.assertEquals(is_user_is_following(self.at3, self.at2), True)
        self.assertEquals(is_user_is_following(self.at3, self.at3), False)
        
        at1_followers_list = get_followers_list(self.at1)
        print( 'at1_followers_list',  at1_followers_list)
        self.assertEquals( self.at1 in at1_followers_list, False)
        self.assertEquals( self.at2 in at1_followers_list, False)
        self.assertEquals( self.at3 in at1_followers_list, True)
        self.assertEquals( self.admin in at1_followers_list, False)
        

        at1_following_list = get_following_list(self.at1)
        print( 'at1_following_list', at1_following_list)
        self.assertEquals( self.at1 in at1_following_list, False)
        self.assertEquals( self.at2 in at1_following_list, False)
        self.assertEquals( self.at3 in at1_following_list, True)
        self.assertEquals( self.admin in at1_following_list, True)

    def test_discussion_invitations(self):
        d , error_string = create_discussion( self.admin, "Visit the moon13", "because i saw this in my bazuka")
        self.assertEquals(d.viewer_set.count(), 1) 
        self.assertEquals(d.can_user_participate( self.at1), True)
        d.is_restricted = True
        d.save()
        self.assertEquals(d.can_user_participate( self.at1), False)
        self.assertEquals(d.viewer_set.count(), 1) 

        dis , error_string =discussion_invite(d, self.at1)
        self.assertEquals(error_string, None) 
        self.assertEquals(d.can_user_participate( self.at1), True) 
        self.assertEquals(d.viewer_set.count(), 2) 
        
        discussion_cancel_invite( d, self.at1)
        self.assertEquals(d.is_user_invited( self.at1), False) 
        self.assertEquals(d.can_user_participate( self.at1), False)
        self.assertEquals(d.viewer_set.count(), 2) 
        
        discussion_invite(d, self.at2)
        self.assertEquals(d.is_user_invited( self.at2), True) 
        self.assertEquals(d.viewer_set.count(), 3) 
        
        followers_list = d.get_followers_list()
        self.assertEquals( self.at3 in followers_list , False)
         
        discussion_invite(d,  self.at3)
        
        invited_users_list  = d.get_invited_users_list()
        self.assertEquals( self.at3 in invited_users_list , True) 
        
        self.assertEquals( len(invited_users_list) , 2) 
        self.assertEquals(d.viewer_set.count(), 4) 
        
        discussion_invite(d, self.at1)
        invited_users_list = d.get_invited_users_list()
        self.assertEquals( len(invited_users_list), 3)
        
        print( 'invited_users_list', invited_users_list)
        
        discussion_cancel_invite( d, self.at2)
        d.print_content()
        
    def test_segments(self):
        print( 'test_segments start')

        self.assertEquals(Segment.objects.count(), 0) 
        
        seg1 = Segment( title ='seg1')
        seg1.save()
        seg2 = Segment( title ='seg2')
        seg2.save()
        self.assertEquals(Segment.objects.count(), 2) 
        
        self.assertEquals( is_in_the_same_segment(self.admin,  self.at1), True)
        self.admin.userprofile.set_segment()
        self.assertEquals( is_in_the_same_segment(self.admin,  self.at1), True)
        print( seg1)
        self.admin.userprofile.set_segment( seg1)

        self.at1.userprofile.print_content()
        self.admin.userprofile.print_content()
        
        self.assertEquals( is_in_the_same_segment(self.admin,  self.at1), False)
        
        self.at1.userprofile.set_segment( seg1)
        self.assertEquals( is_in_the_same_segment(self.admin,  self.at1), True)
        
        self.at2.userprofile.set_segment( seg1)
        self.assertEquals( is_in_the_same_segment(self.admin,  self.at2), True)
        
        self.at2.userprofile.set_segment( seg2)
        self.assertEquals( is_in_the_same_segment(self.admin,  self.at2), False)

        self.assertEquals( is_in_the_same_segment(self.at3,  self.at2), False)
        
        self.at3.userprofile.set_segment( seg2)
        
        self.assertEquals( is_in_the_same_segment(self.at3,  self.at2), True)
        
        admin_all_users_in_same_segment_list = self.admin.userprofile.get_all_users_in_same_segment_list()
        for user in admin_all_users_in_same_segment_list:
            print( user.userprofile.print_content)
        
        at1_all_users_in_same_segment_list = get_all_users_visiabale_for_a_user_list(  self.at1)
        at2_all_users_in_same_segment_list = get_all_users_visiabale_for_a_user_list(  self.at2)
        at4_all_users_in_same_segment_list = get_all_users_visiabale_for_a_user_list(  self.at4)
        
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
                
        d , error_string = create_discussion( self.admin, "Visit the moon14", "because i saw this in my bazuka")
        
        self.assertEquals(d.is_user_in_discussion_segment( self.admin), True) 
        self.assertEquals(d.is_user_in_discussion_segment( self.at1), True) 
        self.assertEquals(d.is_user_in_discussion_segment( self.at2), False) 
        self.assertEquals(d.is_user_in_discussion_segment( self.at4), False) 

    def test_user_update(self):
        print( 'test_user_update start')
        self.assertEquals(UserUpdate.objects.count(), 0)
        d , error_string = create_discussion( self.admin, "Visit the moon15", "because i saw this in my bazuka")
         
        post_update_to_user(self.at1.id, header = 'כותרת', content = 'תוכן', discussion_id = d.id, sender_user_id = self.at2.id,  details_url = 'www.hp.com')
        
        post_update_to_user(self.at1.id, header = '3כותרת', content = '3תוכן', discussion_id = d.id, sender_user_id = self.at3.id,  details_url = 'www.hp.com')

        post_update_to_user(self.at2.id, header = '4כותרת', content = '4תוכן', discussion_id = d.id, sender_user_id = self.at3.id,  details_url = 'www.hp.com')
        
        self.assertEquals(UserUpdate.objects.count(), 3)
        for user_update in UserUpdate.objects.all():
            user_update.print_content()
        
        
    def test_user_glimpse_a_discussion(self):
        print( 'test_user_glimpse_a_discussion')
        d , error_string = create_discussion( self.admin, "Visit the moon16", "because i saw this in my bazuka")
        self.assertEquals(d.viewer_set.count(), 1) 
        discussion_record_a_view(d, self.at1)#no following save - counters shall not incremented     
        
        at1_view = d.viewer_set.get( user = self.at1)
        self.assertEquals(d.viewer_set.count(), 2) 
        self.assertEquals(at1_view.glimpse_set.count(), 1)
        
        discussion_record_a_view(d, self.at1)        
        at1_view = d.viewer_set.get( user = self.at1)
        self.assertEquals(at1_view.glimpse_set.count(), 1)
        self.assertEquals(at1_view.get_views_counter(), 1)
        d.save() 
        discussion_record_a_view(d, self.at1)        
        at1_view = d.viewer_set.get( user = self.at1)
        self.assertEquals(at1_view.glimpse_set.count(), 2)
        self.assertEquals(at1_view.get_views_counter(), 2)        

        d.save() 
        discussion_record_a_view(d, self.at2)        
        d.save() 
        discussion_record_a_view(d, self.at3)        
        d.save() 
        
        discussion_record_a_view(d, self.at1)
        
        self.assertEquals(Glimpse.objects.count(), 5)
        for glimpse in Glimpse.objects.all().order_by("-created_at"):
            glimpse.print_content()

       

    def test_rewards(self):    
        print( 'test_rewards')
        self.assertEquals(0,  self.admin.account.get_credit())
        self.assertEquals(0,  self.at1.account.get_credit())

        d , error_string = create_discussion( self.admin, "Visit the moon16", "because i saw this in my bazuka")
        self.assertEquals(error_string, None)
        self.assertEquals(27,  self.admin.account.get_credit())
        
        feedback, error_string = discussion_add_feedback(d ,self.at1, Feedback.ENCOURAGE, "like this")        
        self.assertEquals(7,  self.at1.account.get_credit())
        
        des1 , error_string = discussion_add_decision(d, self.admin, 'אולי מלמטה?')
        self.assertEquals(error_string, None)
        self.assertEquals(27 + 5,  self.admin.account.get_credit())
        
        decision_vote(des1, self.at1 ,  LikeLevel.EXCELLENT)
        self.assertEquals(7 + 3,  self.at1.account.get_credit())
        
        task2, error_string = discussion_add_task(d ,self.at1, 'shall close9', timezone.now() +  datetime.timedelta(seconds =1))
        
        update_task_state(task2,Task.CLOSED,self.admin)
        task4, error_string = discussion_add_task(d ,self.admin, 'shall close10', timezone.now() +  datetime.timedelta(seconds =1))
        self.assertEquals(error_string, None)
        
        update_task_state(task4,Task.CLOSED,self.at1)
        
        task5, error_string  = discussion_add_task(d ,self.at1, 'shall abort33', timezone.now() +  datetime.timedelta(seconds =1))
        self.assertEquals(error_string, None)
        
        update_task_state(task5,Task.ABORTED,self.admin)
        task6, error_string  = discussion_add_task(d ,self.admin, 'shall shall abort66', timezone.now() +  datetime.timedelta(seconds =1))
        self.assertEquals(error_string, None)
        
        update_task_state(task6,Task.ABORTED,self.at1)
        
        time.sleep(7)        
        poll_for_task_complition(task2)
        poll_for_task_complition(task4)
        poll_for_task_complition(task5)
        poll_for_task_complition(task6)
        
        
        discussion_record_a_view(d, self.at1)
        d.print_content()
        self.admin.account = Account.objects.get(id = self.admin.account.id)
        self.at1.account = Account.objects.get(id = self.at1.account.id)
        self.admin.account.print_content()
        self.at1.account.print_content()        
        print( 'cici')
        self.admin.account.print_content()        
        self.assertEquals(84,  self.admin.account.get_credit())
        self.assertEquals(76,  self.at1.account.get_credit())


