from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

    

class Discussion(models.Model):
    Owner = models.ForeignKey(User, editable = False)
    Title = models.CharField( unique = True, max_length=200)
    Description = models.CharField(blank = True, null = True, max_length=600, validators=[MaxLengthValidator])
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    
    def __unicode__(self):
        return self.id
    def add_response(self, user, ResponseType, TextBody):
        response = Response(discussion = self ,attendant = user, TextBody = TextBody, ResponseType =  ResponseType)
        response.save()
        self.save()

    def add_decision(self, TextBody):
        decision = Decision(discussion = self , TextBody = TextBody)
        decision.save()
        self.save()
        return decision

    def add_action(self, responsible, GoalDescription, input_target_date):
        action  = Action(discussion = self , responsible = responsible, 
                         GoalDescription = GoalDescription, 
                         target_date =  input_target_date)
        action.save()
        self.save()
        return action

   
    def print_content(self):
        print 'Owner', self.Owner.username
        print 'Title:', self.Title
        print 'Description:', self.Description
        responses = self.response_set.all()
        for response in responses:
            response.print_content()
        decisions = self.decision_set.all()
        for decision in decisions:
            decision.print_content()
        actions = self.action_set.all()
        for action in actions:
            action.print_content()
            

class LikeLevel(object):
    EXCELLENT= 5
    VERY_GOOD = 4
    GOOD = 3
    MEDIUM = 2
    BAD = 1
    level = (
               (EXCELLENT, 'Excellent Idea'),
               (VERY_GOOD, 'I realy like it'),
               (GOOD, 'Not Bad'),
               (MEDIUM, 'Not Sure'),
              (BAD, 'Bad Idea'),
              )
    
    
class Decision(models.Model):
    discussion = models.ForeignKey(Discussion)
    TextBody = models.CharField( max_length=200, validators=[MaxLengthValidator],editable =False)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    Value = models.IntegerField( default = 0)
    
    def __unicode__(self):
        return "" + self.id
    def get_number_of_votes(self):
        return self.vote_set.count()
    
    def print_content(self):
        print 'Decide:', self.TextBody, 'create_date', self.create_date, 'value', self.Value
        votes = self.vote_set.all()
        for vote in votes:
            vote.print_content()
            
    def vote(self, Voater, Value):
        if (self.vote_set.filter( Voater= Voater).count() == 0):
            new_vote = Vote(  decision = self, Voater= Voater, Value = Value)
            new_vote.save()
            self.Value += Value
        else:
            current_vote = self.vote_set.get( Voater= Voater)
            self.Value -= current_vote.Value
            current_vote.Value = Value
            self.Value += current_vote.Value
            current_vote.save()
            
        self.save()
"""       
        votes_for_user = self.vote_set.filter( Voater= Voater).count()
        if votes_for_user == 0:
            print 'already', votes_for_user
            
        if self.votes_set.filter( Voater = Voater)
             
        
        votes_for_user = self.vote_set.filter( Voater= Voater).count()
        if votes_for_user != 0:
            print 'already', votes_for_user

        new_vote = Vote(  decision = self, Voater= Voater, Value = Value)
        new_vote.save()
        self.save()
"""    
    
    
    
class Vote(models.Model):
    decision  = models.ForeignKey(Decision )
    Voater = models.ForeignKey(User)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    Value = models.IntegerField( choices =LikeLevel.level, null=True,
                                     blank=True, db_index=True)

    def __unicode__(self):
        return self.id
    def print_content(self):
        print 'voater', self.Voater_id, 'value', self.Value

"""
class Test(models.Model):
#    goal_desc = models.CharField(  max_length=200)
    target_date = models.DateTimeField('Target date' )
#    closing_date = models.DateTimeField('Achived at',blank = True,  null = True, default = 0)
    closing_date = models.DateTimeField('Achived at')    
    StatusDescription = models.TextField(blank=True, null = True)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    def __unicode__(self):
        return self.id
"""

class Action(models.Model):
    STARTED = 'S'
    CLOSED = 'C'
    MISSED = 'M'
    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (CLOSED, 'Closed'),
        (MISSED, 'Missed'),
    )
    
    discussion = models.ForeignKey(Discussion)
    responsible = models.ForeignKey(User)
    GoalDescription = models.CharField(  max_length=200, editable = False)
    target_date = models.DateTimeField('Target date')
    closing_date = models.DateTimeField('Achived at')
    StatusDescription = models.TextField(blank=True, null = True)
    status = models.CharField(max_length=1,
                                      choices=STATUS_CHOICES,
                                      default=STARTED)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    
    def __unicode__(self):
        return "" + self.id
    def print_content(self):
        print 'create', self.create_date, 'update', self.update_date, 'status:', self.get_status(), 'now', timezone.now(), 'GoalDescription:', self.GoalDescription, 'target_date:', self.target_date, 'remaining', self.get_time_until_target(), 'closing_date:', self.closing_date, self.StatusDescription 
    def update_status_description(self, StatusDescription):
        self.StatusDescription = StatusDescription
        self.save()
    def close(self):
        self.refresh_status()
        if (self.status == self.STARTED):
            self.status = self.CLOSED
            self.closing_date = timezone.now() 
            self.save()

        
    def get_time_until_target(self):
        self.refresh_status()
        if ( self.status == self.STARTED):
            return  self.target_date - timezone.now() 
        return 0
    def refresh_status(self):
        if (self.status == self.CLOSED):
            return
        if (self.status == self.MISSED):
            return
            
        if (self.target_date < timezone.now() ):
            self.status = self.MISSED
            self.save()
            
    def get_status(self):
        self.refresh_status()
        return self.status
        
class Response(models.Model):
    RESPONSE_TYPES  = (
        ('E','Encourage'  ),
        ('C','Cooperation'),
        ('I','Intuition'  ), 
        ('A','Advise'     ),
    )
    
    discussion = models.ForeignKey(Discussion)
    attendant = models.ForeignKey(User, verbose_name="Attendant",  db_index=True)
    ResponseType = models.CharField(max_length=1, choices=RESPONSE_TYPES, db_index=True)
    TextBody = models.CharField(  max_length=600, validators=[MaxLengthValidator] )
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    def __unicode__(self):
        return self.id
    def print_content(self):
        print self.attendant_id, 'said a ResponseType', self.ResponseType, 'That:', self.TextBody, 'create_date', self.create_date 
 

        
        
            
        
        

    