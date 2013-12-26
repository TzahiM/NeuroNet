from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models

MAX_TEXT = 2000


class Discussion(models.Model):
    owner = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id


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
    type = models.IntegerField(choices=FEEDBACK_TYPES)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content


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

    def __unicode__(self):
        return self.content


class Vote(models.Model):
    user = models.ForeignKey(User)
    decision = models.ForeignKey(Decision)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(choices=LikeLevel.level)

    class Meta:
        unique_together = (
                           ('user', 'decision'),
                           )

    def __unicode__(self):
        return "{} - {}: {}".format(self.decision, self.user, self.value)

    def print_content(self):
        print 'voater', self.Voater_id, 'value', self.Value


class Task(models.Model):

    STARTED = 1
    CLOSED = 2
    MISSED = 3

    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (CLOSED, 'Closed'),
        (MISSED, 'Missed'),
    )

    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    target_date = models.DateField()
    closed_at = models.DateTimeField(null=True, blank=True)
    status_description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content
