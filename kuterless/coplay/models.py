# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import ugettext as _

MAX_TEXT = 2000

MAX_INACTIVITY_SECONDS = 7 * 24 * 3600


class Discussion(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    locked_at = models.DateTimeField(default=None, blank=True, null=True)

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return (
        reverse('coplay:discussion_details', kwargs={'pk': str(self.id)}) )

    def update_description(self, description):
        self.description = description
        self.save()#cause all previous fedbacks to be striked at

    def add_feedback(self, user, feedbabk_type, content):
        feedback = Feedback(discussion=self, user=user,
                            feedbabk_type=feedbabk_type, content=content)
        feedback.clean()
        feedback.save()
        return feedback


    def add_decision(self, content):
        decision = Decision(parent=self, content=content)
        decision.clean()
        decision.save()
        return decision


    def add_task(self, responsible, goal_description, target_date,
                 max_inactivity_seconds=MAX_INACTIVITY_SECONDS):
        self.locked_at = timedelta(
            seconds=max_inactivity_seconds) + timezone.now()
        task = self.task_set.create(parent=self, responsible=responsible,
                                    goal_description=goal_description,
                                    target_date=target_date)
        self.save()
        task.clean()
        task.save()
        return task

    def is_active_and_time_to_inactivation_obsolete(self,
                                                    max_inactivity_seconds=MAX_INACTIVITY_SECONDS):
        now = timezone.now()
        list_tasks = self.task_set.all().order_by("-created_at")
        if list_tasks:
            latest_task = list_tasks.first()
            if (latest_task.created_at + timedelta(
                    seconds=max_inactivity_seconds) ) >= now:
                time_left = (latest_task.created_at + timedelta(
                    seconds=max_inactivity_seconds) ) - now
                discussion_is_active = True
                return discussion_is_active, time_left
            if (self.created_at + timedelta(
                    seconds=max_inactivity_seconds) ) >= now:
                discussion_is_active = True
                time_left = (self.created_at + timedelta(
                    seconds=max_inactivity_seconds) ) - now
                return discussion_is_active, time_left
            discussion_is_active = False
            time_left = 0
            return discussion_is_active, time_left
        if (self.created_at + timedelta(
                seconds=max_inactivity_seconds) ) >= now:
            discussion_is_active = True
            time_left = (self.created_at + timedelta(
                seconds=max_inactivity_seconds) ) - now
            return discussion_is_active, time_left

        discussion_is_active = False
        time_left = 0
        return discussion_is_active, time_left


    def is_active_and_time_to_inactivation(self,
                                           max_inactivity_seconds=MAX_INACTIVITY_SECONDS):
        now = timezone.now()
        if self.locked_at is None:#init self.created_at for the first time
            discussion_is_active, time_left = self.is_active_and_time_to_inactivation_obsolete(
                max_inactivity_seconds)
            if discussion_is_active:
                self.locked_at = now + time_left
                self.save();
                return discussion_is_active, time_left
            list_tasks = self.task_set.all().order_by("-created_at")
            if list_tasks:
                latest_task = list_tasks.first()
                self.locked_at = latest_task.created_at + timedelta(
                    seconds=max_inactivity_seconds)
                self.save();
                return discussion_is_active, time_left

            self.locked_at = self.created_at + timedelta(
                seconds=max_inactivity_seconds)
            self.save();
            return discussion_is_active, time_left

        if now >= self.locked_at:
            discussion_is_active = False
            time_left = 0
            return discussion_is_active, time_left

        discussion_is_active = True

        time_left = self.locked_at - now

        return discussion_is_active, time_left


    def is_active(self):
        discussion_is_active, time_left = self.is_active_and_time_to_inactivation()
        return discussion_is_active

    def get_time_to_inactivation(self):
        discussion_is_active, time_left = self.is_active_and_time_to_inactivation()
        return time_left

    def get_attending_list(self, include_owner=False):
        users_list = []
        for feedback in self.feedback_set.all():
            if feedback.user not in users_list:
                users_list.append(feedback.user)
        for task in self.task_set.all():
            if task.responsible not in users_list:
                users_list.append(task.responsible)
        for descision in self.decision_set.all():
            for vote in descision.vote_set.all():
                if vote.voater not in users_list:
                    users_list.append(vote.voater)

        if include_owner:
            if self.owner not in users_list:
                users_list.append(self.owner)
        else:
            if self.owner in users_list:
                users_list.remove(self.owner)

        return users_list


    def print_content(self):
        print 'Owner', self.owner.username
        print 'Title:', self.title
        print 'Description:', self.description
        discussion_is_active, time_left = self.is_active_and_time_to_inactivation()
        if discussion_is_active:
            print 'active, time left', time_left
        else:
            print 'inactivated'

        print 'attending:'
        attending_list = self.get_attending_list()
        for user in attending_list:
            print user.username

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
        (ENCOURAGE, 'עידוד'),
        (COOPERATION, 'שיתוף פעולה'),
        (INTUITION, 'אינטואיציה'),
        (ADVICE, 'עצה'),
    )

    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    feedbabk_type = models.IntegerField(choices=FEEDBACK_TYPES)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content


    def get_feedbabk_type_name(self):
        feedbabk_type = self.feedbabk_type
        if feedbabk_type == self.ENCOURAGE:
            return 'עידוד'
        if feedbabk_type == self.COOPERATION:
            return 'פעולה'
        if feedbabk_type == self.INTUITION:
            return 'אינטואיציה'
        return 'עצה'


    def print_content(self):
        print self.user.username, 'said a ResponseType', self.feedbabk_type, 'That:', self.content, 'created_at', self.created_at, 'updated', self.updated_at

    def get_absolute_url(self):
        return self.discussion.get_absolute_url()


class LikeLevel(object):
    EXCELLENT = 5
    VERY_GOOD = 4
    GOOD = 3
    MEDIUM = 2
    BAD = 1
    level = (
        (EXCELLENT, 'רעיון מצוייו'),
        (VERY_GOOD, 'טוב מאוד'),
        (GOOD, 'לא רע'),
        (MEDIUM, 'אין דעה'),
        (BAD, 'רעיון לא טוב'),
    )


class Decision(models.Model):
    parent = models.ForeignKey(Discussion)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content

    def get_number_of_votes(self):
        return self.vote_set.count()

    def vote(self, voater, value):
        if (self.vote_set.filter(voater=voater).count() == 0):
            new_vote = Vote(decision=self, voater=voater, value=value)
            new_vote.save()
            self.value += value
        else:
            current_vote = self.vote_set.get(voater=voater)
            self.value -= current_vote.value
            current_vote.value = value
            self.value += current_vote.value
            current_vote.save()

        self.save()

    def get_vote_sum(self):
        return (self.value)

    def get_vote_value_or_none(self, voater):
        if self.vote_set.filter(voater=voater).count() == 1:
            vote = self.vote_set.get(voater=voater)
            return vote.value
        return None

    def get_vote_average_or_none(self):
        number_of_votes = self.get_number_of_votes()
        if number_of_votes != 0:
            average = int(round(self.get_vote_sum() / number_of_votes))
            return average
        return None

    def get_vote_level_name(self):
        number_of_votes = self.get_vote_average_or_none()
        if number_of_votes:
            if number_of_votes == LikeLevel.EXCELLENT:
                return 'מצויין'
            if number_of_votes == LikeLevel.VERY_GOOD:
                return 'טוב מאוד'
            if number_of_votes == LikeLevel.GOOD:
                return 'טוב'
            if number_of_votes == LikeLevel.MEDIUM:
                return 'אין דעה'
            if number_of_votes == LikeLevel.BAD:
                return 'רעיון לא טוב'

        return 'אין'

        return self.vote_set.count()

    def print_content(self):
        print 'Decide:', self.content, 'created_at', self.created_at, 'value', self.value
        votes = self.vote_set.all()
        for vote in votes:
            vote.print_content()

    def get_absolute_url(self):
        return self.parent.get_absolute_url()


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
        (STARTED, 'בדרך'),
        (CLOSED, 'הושלמה'),
        (MISSED, 'פוספסה'),
    )

    parent = models.ForeignKey(Discussion, null=True, blank=True)
    responsible = models.ForeignKey(User)
    goal_description = models.TextField(
        validators=[MaxLengthValidator(MAX_TEXT)])
    target_date = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(User, related_name='closed_by', null=True,
                                  blank=True)
    status_description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content


    def get_absolute_url(self):
        return ( reverse('coplay:task_details', kwargs={'pk': str(self.id)}) )


    def update_status_description(self, status_description):
        self.refresh_status()
        if self.status != self.STARTED:
            return False
        self.status_description = status_description
        self.save()
        return True

    def get_status_description(self):
        return self.status_description

    def close(self, closing_user):
        if self.responsible is closing_user:
            return False
        self.refresh_status()
        if (self.status == self.STARTED):
            self.status = self.CLOSED
            self.closed_at = timezone.now()
            self.closed_by = closing_user
            self.save()
            return True
        return False


    def get_time_until_target(self):
        self.refresh_status()
        if ( self.status == self.STARTED):
            return self.target_date - timezone.now()
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
        print 'create', self.created_at, 'update', self.updated_at, 'status:', self.get_status_display(), 'now', timezone.now(), 'GoalDescription:', self.goal_description, 'target_date:', self.target_date, 'remaining', self.get_time_until_target(), 'closing_date:', self.closed_at, self.status_description
