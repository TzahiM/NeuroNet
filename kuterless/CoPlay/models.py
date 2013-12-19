from django.core.validators import MaxLengthValidator
from django.db import models

# Create your models here.

class Attendant(models.Model):
    name = models.CharField( unique = True, db_index=True, max_length=200, validators=[MaxLengthValidator])

    def __unicode__(self):
        return self.name
    
class Discussion(models.Model):
    Owner = models.ForeignKey(Attendant, editable =False)
    Title = models.CharField( unique = True, max_length=200, validators=[MaxLengthValidator], editable =False)
    Description = models.CharField(blank = True, Null = True, max_length=600, validators=[MaxLengthValidator])
    create_date = models.DateTimeField('date created', auto_now_add=True )

    def __unicode__(self):
        return self.id

class Response(models.Model):
    RESPONSE_TYPES  = (
        ('E','Encourage'  )
        ('C','Cooperation'),
        ('I','Intuition'  ), 
        ('A','Advise'     ),
    )
    
    attendant = models.OneToOneField(Attendant, verbose_name="Attendant",  db_index=True, editable =False)
    TextBody = models.CharField(  max_length=200, validators=[MaxLengthValidator],editable =False)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    ResponseType = models.CharField(max_length=1, choices=RESPONSE_TYPES, editable =False)
    discussion = models.ForeignKey(Discussion   )
    def __unicode__(self):
        return self.id

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
    TextBody = models.CharField( max_length=200, validators=[MaxLengthValidator],editable =False)
    discussion  = models.ForeignKey(Discussion )
    create_date = models.DateTimeField('date created', auto_now_add=True )

    def __unicode__(self):
        return self.id
    
    
class Vote(models.Model):
    decision  = models.ForeignKey(Decision )
    Voater = models.OneToOneField(Attendant, editable =False)
    create_date = models.DateTimeField('date created', auto_now_add=True )
    Value = models.IntegerField(choices=LikeLevel.choices, null=True,
                                     blank=True, db_index=True)

    def __unicode__(self):
        return self.id
    




    