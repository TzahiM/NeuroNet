from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models

# Create your models here.

    

class Discussion(models.Model):
    Owner = models.ForeignKey(User)
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


class LikeLevel(object):
    EXCELLENT= 5
    VERY_GOOD = 4
    GOOD = 3
    MEDIUM = 2
    BAD = 1
    NOT_DEFINED = 0
    level = (
               (EXCELLENT, 'Excellent Idea'),
               (VERY_GOOD, 'I realy like it'),
               (GOOD, 'Not Bad'),
               (MEDIUM, 'Not Sure'),
              (BAD, 'Bad Idea'),
              (NOT_DEFINED, 'Please Choose'),              
              )
    
    
class Decision(models.Model):
    discussion = models.ForeignKey(Discussion)
    TextBody = models.CharField( max_length=200, validators=[MaxLengthValidator],editable =False)
    create_date = models.DateTimeField('date created', auto_now_add=True )

    def __unicode__(self):
        return self.id
    def print_content(self):
        print 'Decide:', self.TextBody, 'create_date', self.create_date 
    
    
    
    
    
class Vote(models.Model):
    decision  = models.ForeignKey(Decision )
    Voater = models.ForeignKey(User)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    Value = models.IntegerField( default=LikeLevel.NOT_DEFINED, choices =LikeLevel.level, null=True,
                                     blank=True, db_index=True)

    def __unicode__(self):
        return self.id
    

class Action(models.Model):
    discussion = models.ForeignKey(Discussion)
    responsible = models.ForeignKey(User)
    GoalDescription = models.CharField(  max_length=200)
    target_date = models.DateTimeField('Should be completed untill')
    closing_date = models.DateTimeField('Achived at',blank = True,  null = True)
    StatusDescription = models.TextField(blank=True, null = True)
    def __unicode__(self):
        return self.id

class Witness(models.Model):
    responsible = models.ForeignKey(User)
    action = models.ForeignKey(Action)

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
 

        
        
            
        
        

    