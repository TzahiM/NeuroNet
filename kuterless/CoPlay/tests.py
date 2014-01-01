# -*- coding: utf-8 -*-
from coplay.models import Discussion, Feedback, Decision, LikeLevel, Vote, Task
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
import datetime
import time


class CoPlayTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user('admin', 'user1@example.com',
                                              'secret')
        self.at1 = User.objects.create_user('at1', 'user1@example.com',
                                              'secret')
        self.at2 = User.objects.create_user('at2', 'user1@example.com',
                                              'secret')
        self.at3 = User.objects.create_user('at3', 'user1@example.com',
                                              'secret')


    def create_dicussion(self):
        d = Discussion()
        d.owner = self.admin
        d.title = "Visit the moon"
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
        self.assertEquals(3, Task.objects.count())
        time.sleep(1)
        task2.close(self.admin)
        time.sleep(2)
        self.assertEquals(self.admin, task2.closed_by)
        self.assertEquals(False, task1.close(self.at1))
        self.assertEquals(task1.STARTED, task1.get_status())
        self.assertEquals(task1.CLOSED, task2.get_status())
        self.assertEquals(task1.MISSED, task3.get_status())
        new_stat_desc = "fjfj"
        task1.update_status_description(new_stat_desc)
        self.assertEquals(task1.get_status_description(), new_stat_desc)
        new_stat_desc = "dfasgg"
        task1.close(self.admin)
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
        d.print_content()
        d2.print_content()


