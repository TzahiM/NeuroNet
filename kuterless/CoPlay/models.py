from django.core.validators import MaxLengthValidator
from django.db import models

# Create your models here.

class Attendant(models.Model):
    name = models.CharField( unique = True, db_index=True, max_length=20, validators=[MaxLengthValidator])

    def __unicode__(self):
        return self.name
    


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
    TextBody = models.CharField( max_length=200, validators=[MaxLengthValidator],editable =False)
    create_date = models.DateTimeField('date created', auto_now_add=True )

    def __unicode__(self):
        return self.id
    
    
class Vote(models.Model):
    decision  = models.ForeignKey(Decision, editable =False )
    Voater = models.ForeignKey(Attendant, editable =False)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    Value = models.IntegerField( default=LikeLevel.NOT_DEFINED, choices =LikeLevel.level, null=True,
                                     blank=True, db_index=True)

    def __unicode__(self):
        return self.id
    

class Action(models.Model):
    responsible = models.OneToOneField(Attendant, verbose_name="Responsible")
    Witnesses = models.ManyToManyField( Attendant, related_name='w+')
    GoalDescription = models.CharField(  max_length=200, validators=[MaxLengthValidator])
    target_date = models.DateTimeField('Should be completed untill')
    closing_date = models.DateTimeField('Achived at',blank = True,  null = True)
    StatusDescription = models.TextField(blank=True, null = True)
    def __unicode__(self):
        return self.id

class Response(models.Model):
    RESPONSE_TYPES  = (
        ('E','Encourage'  ),
        ('C','Cooperation'),
        ('I','Intuition'  ), 
        ('A','Advise'     ),
    )
    
    
    attendant = models.ForeignKey(Attendant, verbose_name="Attendant",  db_index=True)
    ResponseType = models.CharField(max_length=1, choices=RESPONSE_TYPES, db_index=True)
    TextBody = models.CharField(  max_length=600, validators=[MaxLengthValidator] )
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    def __unicode__(self):
        return self.id


class Discussion(models.Model):
    Owner = models.ForeignKey(Attendant)
    Title = models.CharField( unique = True, max_length=200, validators=[MaxLengthValidator])
    Description = models.CharField(blank = True, null = True, max_length=600, validators=[MaxLengthValidator])
    create_date = models.DateTimeField('date created', auto_now_add=True )
    update_date = models.DateTimeField('last-modifie', auto_now =True )
    Responses   = models.ManyToManyField(Response, related_name='r+', blank = True, null = True)
    Actions   = models.ManyToManyField(Action, related_name='a+', blank = True, null = True)
    Decisions   = models.ManyToManyField(Decision, related_name='d+',blank = True, null = True)
    
    def __unicode__(self):
        return self.id
        
        
            
        
        

    