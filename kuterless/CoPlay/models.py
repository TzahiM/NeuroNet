from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone

MAX_TEXT = 2000


class Discussion(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id
    
    def update_description(self, description):
        self.description = description
        self.save()

    def add_feedback(self, user, feedbabk_type, content):
        feedback = Feedback(discussion = self ,user = user, feedbabk_type = feedbabk_type, content = content )
        feedback.save()
        self.save()
        return feedback


    def add_decision(self, content):
        decision = Decision(parent = self , content = content)
        decision.save()
        self.save()
        return decision



    def add_task(self, responsible, goal_description, target_date):
        task  = Task(parent = self , responsible = responsible, 
                         goal_description = goal_description, 
                         target_date =  target_date)
        task.save()
        self.save()
        return task

   
    def print_content(self):
        print 'Owner', self.owner.username
        print 'Title:', self.title
        print 'Description:', self.description
        feedbacks = self.feedback_set.all()
        for feedback in feedbacks:
            feedback.print_content()
        decisions = self.decision_set.all()
        for decision in decisions:
            decision.print_content()
        tasks = self.task_set.all()
        for task in tasks:
            task.print_content()

class Feedback(models.Model):

    ENCOURAGE = 1
    COOPERATION = 2
    INTUITION = 3
    ADVICE = 4

    FEEDBACK_TYPES = (
        (ENCOURAGE, 'Encourage'),
        (COOPERATION, 'Cooperation'),
        (INTUITION, 'Intuition'),
        (ADVICE, 'Advice'),
    )

    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    feedbabk_type = models.IntegerField(choices=FEEDBACK_TYPES)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

    def print_content(self):
        print self.user.username, 'said a ResponseType', self.feedbabk_type, 'That:', self.content, 'created_at', self.created_at, 'updated', self.updated_at 



class LikeLevel(object):
    EXCELLENT = 5
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
    parent = models.ForeignKey(Discussion)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField( default = 0)

    def __unicode__(self):
        return self.content
    def get_number_of_votes(self):
        return self.vote_set.count()
    def vote(self, voater, value):
        if (self.vote_set.filter( voater= voater).count() == 0):
            new_vote = Vote(  decision = self, voater= voater, value = value)
            new_vote.save()
            self.value += value
        else:
            current_vote = self.vote_set.get( voater= voater)
            self.value -= current_vote.value
            current_vote.value = value
            self.value += current_vote.value
            current_vote.save()
            
        self.save()
        
    def get_vote_sum(self):
        return(self.value)
    def print_content(self):
        print 'Decide:', self.content, 'created_at', self.created_at, 'value', self.value
        votes = self.vote_set.all()
        for vote in votes:
            vote.print_content()
        


class Vote(models.Model):
    voater = models.ForeignKey(User)
    decision = models.ForeignKey(Decision)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(choices=LikeLevel.level)

    class Meta:
        unique_together = (
                           ('voater', 'decision'),
                           )

    def __unicode__(self):
        return "{} - {}: {}".format(self.decision, self.voater, self.value)

    def print_content(self):
        print 'voater', self.voater.username, 'value', self.value


class Task(models.Model):

    STARTED = 1
    CLOSED = 2
    MISSED = 3

    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (CLOSED, 'Closed'),
        (MISSED, 'Missed'),
    )

    parent = models.ForeignKey(Discussion)
    responsible = models.ForeignKey(User)
    goal_description = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    target_date = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    status_description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content
    
    def update_status_description(self, status_description):
        self.status_description = status_description
        self.save()

    def get_status_description(self):
        return self.status_description
        
    def close(self):
        self.refresh_status()
        if (self.status == self.STARTED):
            self.status = self.CLOSED
            self.closed_at = timezone.now() 
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
        
        
    def print_content(self):
        print 'create', self.created_at, 'update', self.updated_at, 'status:', self.get_status(), 'now', timezone.now(), 'GoalDescription:', self.goal_description, 'target_date:', self.target_date, 'remaining', self.get_time_until_target(), 'closing_date:', self.closed_at, self.status_description 
