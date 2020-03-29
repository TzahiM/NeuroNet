# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


MAX_TEXT = 2000

MAX_INACTIVITY_SECONDS = 7 * 24 * 3600


class Location(models.Model):
    num = models.IntegerField()
    street = models.CharField(max_length=100, default=None, blank=True, null=True)
    city = models.CharField(max_length=100, default=None, blank=True, null=True)
    state = models.CharField(max_length=20, default = u'ישראל', blank=True)
    latitude    = models.FloatField(default=None, blank=True, null=True)
    longitude   = models.FloatField(default=None, blank=True, null=True)

class Discussion(models.Model):
    owner                       = models.ForeignKey(User, on_delete = models.CASCADE)
    title                       = models.CharField(_("title"), max_length=200)
    description                 = models.TextField(_("Description"), blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    created_at                  = models.DateTimeField(auto_now_add=True)
    updated_at                  = models.DateTimeField(auto_now=True)
    locked_at                   = models.DateTimeField(default=None, blank=True, null=True)
    description_updated_at      = models.DateTimeField(default=None, blank=True, null=True)
    is_restricted               = models.BooleanField(default = False)
    is_viewing_require_login    = models.BooleanField(default = False)
    location                    = models.ForeignKey(Location, null=True, blank=True, on_delete = models.SET_NULL)
    latitude                    = models.FloatField(default=None, blank=True, null=True)
    longitude                   = models.FloatField(default=None, blank=True, null=True)
    location_desc               = models.CharField( max_length=200,default=None, blank=True, null=True)
    tags                        = TaggableManager(blank=True)
    parent_url                  = models.URLField( max_length=MAX_TEXT,default=None, blank=True, null=True)                                                   
    parent_url_text             = models.CharField( max_length=MAX_TEXT,default=None, blank=True, null=True)
    picture                     = models.ImageField( upload_to='uploads/%Y/%m/%d/', null=True, blank=True,default = None,max_length = 50000)
    anyway_progress_status      = models.IntegerField(default=None, blank=True, null=True)
    anyway_discuss_id           = models.IntegerField(default=None, blank=True, null=True)
    movie_url                   = models.URLField( max_length=MAX_TEXT,default=None, blank=True, null=True)                                                   
    movie_url_url_text          = models.CharField( max_length=MAX_TEXT,default=None, blank=True, null=True)


    def __str__(self):
        return self.id


    def get_absolute_url(self):
        #return str(self.id)+"/discussion_details/"
        return (
            reverse('coplay:discussion_details', kwargs={'pk': str(self.id)}) 
            )


    def update_description_obs(self, description, location_desc = None, tags_string = None):
        self.description = description
        self.location_desc = location_desc
        tags_list =  tags_string.split(',')
        for tag in tags_list:
            self.tags.add( tag)
        
        self.description_updated_at = timezone.now()
        self.save()#cause all previous fedbacks to be striked at

    def add_feedback_obs(self, user, feedbabk_type, content):
        feedback = Feedback(discussion=self, user=user,
                            feedbabk_type=feedbabk_type, content=content)
        feedback.clean()
        feedback.save()
#         control.user_posted_a_feedback_in_another_other_user_s_discussion(user, feedback.get_absolute_url())
        
        
        return feedback


    def add_decision_obs(self, content):
        decision = Decision(parent=self, content=content)
        decision.clean()
        decision.save()
        return decision


    def add_task_obs(self, responsible, goal_description, target_date,
                 max_inactivity_seconds=MAX_INACTIVITY_SECONDS):
        
        
        task = self.task_set.create(parent=self, responsible=responsible,
                                    goal_description=goal_description,
                                    target_date=target_date)
        task.clean()
        task.save()
        self.unlock(max_inactivity_seconds)
        return task
    
    def unlock(self,max_inactivity_seconds=MAX_INACTIVITY_SECONDS):
        self.locked_at = timedelta(
            seconds=max_inactivity_seconds) + timezone.now()
        self.save()

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

    def get_followers_list(self):
        followers_list = []
        for viewer in self.viewer_set.all():
            if viewer.get_is_a_follower():
                followers_list.append(viewer.user)


        return followers_list

    def record_a_view_obs(self, viewing_user):
        if viewing_user in User.objects.all():
            viewer = self.viewer_set.get_or_create( user = viewing_user)[0]
            viewer.increment_views_counter()


    def record_anonymous_view_obs(self, request):
        
                
        if 'anonymous_user_id' in request.session:
            if AnonymousVisitor.objects.filter( id = int(request.session['anonymous_user_id'])).count() != 0:
                anonymous_user = AnonymousVisitor.objects.get( id = int(request.session['anonymous_user_id']))
            else:
                anonymous_user = AnonymousVisitor()
                anonymous_user.save()
            
            anonymous_viewer = self.anonymousvisitorviewer_set.get_or_create( anonymous_visitor = anonymous_user)[0]
            
            if request.user.is_authenticated:
                anonymous_user.user = request.user;
                anonymous_user.save()
            else:
                anonymous_viewer.increment_views_counter()
        else:
            if request.user.is_authenticated:
                return
            anonymous_user = AnonymousVisitor()
            anonymous_user.save()
            anonymous_viewer = self.anonymousvisitorviewer_set.get_or_create( anonymous_visitor = anonymous_user)[0]
            anonymous_viewer.increment_views_counter()
            
        
        request.session['anonymous_user_id'] = anonymous_user.id

            
    def start_follow_obs( self, viewing_user):
        if viewing_user in User.objects.all():
            viewer = self.viewer_set.get_or_create( user = viewing_user)[0]
            viewer.start_follow_obs()

    def stop_follow_obs(self, viewing_user):
        if viewing_user in User.objects.all():
            viewer = self.viewer_set.get_or_create( user = viewing_user)[0]
            viewer.stop_follow()

    def is_a_follower(self, viewing_user):
        if not viewing_user:
            return False
        if viewing_user.is_authenticated == False:
            return False
        if self.viewer_set.all().filter( user = viewing_user).count() != 0:
            viewer = self.viewer_set.get( user = viewing_user)
            return viewer.get_is_a_follower()
        return False

    def is_user_invited(self, viewing_user) :
                        
        return self.viewer_set.all().filter( user = viewing_user, is_invited  = True).count() != 0
            
    def can_user_participate(self, viewing_user = None):
        
        if self.owner == viewing_user:
            return True
                
        if not self.is_restricted:
            return True
        
        if not viewing_user:
            return False
        
        return self.is_user_invited(viewing_user)

    def get_is_viewing_require_login(self):
        return self.is_viewing_require_login
    
    def is_user_in_discussion_segment(self, viewing_user = None):
                
        if not self.owner.userprofile.is_in_the_same_segment(viewing_user):
            return False
        
        return True
    
    def can_user_access_discussion(self, viewing_user = None):
        
        if self.owner == viewing_user:
            return True
        if self.is_viewing_require_login and viewing_user == None:
            return False
        
        if not self.is_user_in_discussion_segment(viewing_user):
            return False

        if not self.can_user_participate(viewing_user):
            return False
        
        return True

    def invite_obs(self, invited_user):
        if invited_user in User.objects.all():
            viewer = self.viewer_set.get_or_create( user = invited_user)[0]
            viewer.invite()


    def cancel_invitation_obs(self, invited_user):
        if invited_user in User.objects.all():
            viewer = self.viewer_set.get_or_create( user = invited_user)[0]
            viewer.cancel_invitation_obs()

        
    def get_invited_users_list(self):

        invited_users_list = []
        for viewer in self.viewer_set.all():
            if viewer.get_is_invited():
                invited_users_list.append(viewer.user)
                
        return invited_users_list

    def get_discussion(self):
        return self
            
    def print_content(self):
        print( 'Owner', self.owner.username)
        print( 'Title:', self.title)
        print( 'Description:', self.description)
        discussion_is_active, time_left = self.is_active_and_time_to_inactivation()
        if discussion_is_active:
            print( 'active, time left', time_left)
        else:
            print( 'inactivated')
        
        if self.is_restricted:
            print( 'is_restricted. only invited users can view and participate')
        
        if self.is_viewing_require_login:
            print( 'is_viewing_require_login. only logged in users may view')
        
        print( 'attending:')
        attending_list = self.get_followers_list()
        for user in attending_list:
            print( user.username)

        feedbacks = self.feedback_set.all()
        for feedback in feedbacks:
            feedback.print_content()
        decisions = self.decision_set.all()
        for decision in decisions:
            decision.print_content()
        tasks = self.task_set.all()
        for task in tasks:
            task.print_content()
        viewers = self.viewer_set.all()
        for viewer in viewers:
            viewer.print_content()

        anonymous_viewers = self.anonymousvisitorviewer_set.all()
        for anonymous_viewer in anonymous_viewers:
            anonymous_viewer.print_content()

class Feedback(models.Model):
    ENCOURAGE = 1
    COOPERATION = 2
    INTUITION = 3
    ADVICE = 4

    FEEDBACK_TYPES = (
        (ENCOURAGE, u'עידוד'),
        (COOPERATION, u'שיתוף פעולה'),
        (INTUITION, u'אינטואיציה'),
        (ADVICE, u'עצה'),
    )

    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedbabk_type = models.IntegerField(_(u"סוג התגובה"),choices=FEEDBACK_TYPES)
    content = models.TextField(_(u"תוכן התגובה"),validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    voice_recording = models.FileField( _(u"הקלטה"),upload_to='uploads/%Y/%m/%d/', null=True, blank=True,
                                        max_length = 5000000)

        
    def __str__(self):
        return self.content


    def get_feedbabk_type_name(self):
        feedbabk_type = self.feedbabk_type
        if feedbabk_type == self.ENCOURAGE:
            return 'עידוד'
        if feedbabk_type == self.COOPERATION:
            return 'שיתוף פעולה'
        if feedbabk_type == self.INTUITION:
            return 'אינטואיציה'
        return 'עצה'


    def print_content(self):
        print( self.user.username, 'said a ResponseType', self.feedbabk_type, 'That:', self.content, 'created_at', self.created_at, 'updated', self.updated_at)

    def get_absolute_url(self):
        return self.discussion.get_absolute_url()
    
    def get_discussion(self):
        return self.discussion


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
    parent = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    content = models.TextField(validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    def get_number_of_votes(self):
        return self.vote_set.count()

    def vote_obs(self, voater, value):
        if voater == self.parent.owner:
            return False
        if (self.vote_set.filter(voater=voater).count() == 0):
            new_vote = Vote(decision=self, voater=voater, value=value)
            new_vote.save()
            self.value += value
            self.save()
            return True
#             control.user_voted_for_an_idea_in_another_user_s_discussion(voater , self.get_absolute_url())
        current_vote = self.vote_set.get(voater=voater)
        self.value -= current_vote.value
        current_vote.value = value
        self.value += current_vote.value
        current_vote.save()

        self.save()
        return False

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
        print( 'Decide:', self.content, 'created_at', self.created_at, 'value', self.value)
        votes = self.vote_set.all()
        for vote in votes:
            vote.print_content()

    def get_absolute_url(self):
        return self.parent.get_absolute_url() + '#Decisions'

    def get_discussion(self):
        return self.parent

class Vote(models.Model):
    voater = models.ForeignKey(User, on_delete=models.CASCADE)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(choices=LikeLevel.level)

    class Meta:
        unique_together = (
            ('voater', 'decision'),
        )



    def __str__(self):
        return "{} - {}: {}".format(self.decision, self.voater, self.value)

    def print_content(self):
        print( 'voater', self.voater.username, 'value', self.value)

    def get_discussion(self):
        return self.decision.parent

class Task(models.Model):
    STARTED = 1
    CLOSED = 2
    MISSED = 3
    ABORTED = 4
    DISCUSSION_OWNER_COMPLETED = 6
    OTHER_COMPLETED = 7
    DISCUSSION_OWNER_ABORTED = 8
    OTHER_ABORTED = 9
    OTHER_CONFIRMED = 10
    
    STATUS_CHOICES = (
        (STARTED, 'פעילה'),
        (CLOSED, 'הושלמה בהצלחה'),
        (MISSED, 'פוספסה'),
        (ABORTED, 'בוטלה בזמן'),
    )

    parent = models.ForeignKey(Discussion, null=True, blank=True, on_delete=models.CASCADE)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_description = models.TextField(
        validators=[MaxLengthValidator(MAX_TEXT)])
    target_date = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(User, related_name='closed_by', null=True,
                                  blank=True, on_delete=models.SET_NULL)
    status_description = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    final_state    = models.BooleanField(default = False)
    result_picture = models.ImageField( _(u"תמונה של התוצאה"),upload_to='uploads/%Y/%m/%d/', null=True, blank=True,default = None,
                                        max_length = 50000)

    def __str__(self):
        return self.goal_description


    def get_absolute_url(self):
        return ( reverse('coplay:task_details', kwargs={'pk': str(self.id)}) )


    def update_status_description_obs(self, status_description):
#         self.refresh_status()
        if self.final_state:
            return False
        self.status_description = status_description
        self.save()
        return True

    def get_status_description(self):
#         self.refresh_status()
        return self.status_description


    def set_state_obs(self, new_state, closing_user):         
#         self.refresh_status()
        if self.final_state:
            return False
        
        if self.responsible is closing_user:
            return False
        
        
        if (self.status != new_state):
            self.status = new_state
            self.closed_at = timezone.now()
            self.closed_by = closing_user
            self.save()
            return True
        return False

    def abort_obs(self, closing_user):
        
        return self.set_state(self.ABORTED, closing_user)
        

    def re_open_obs(self, closing_user):
        
        return self.set_state(self.STARTED, closing_user)


    def close_obs(self, closing_user):
        
        return self.set_state(self.CLOSED, closing_user)
        


    def get_time_until_target(self):
#         self.refresh_status()
        if self.final_state:
            return 0
        
        return self.target_date - timezone.now()
    

    def poll_status(self):
        now = timezone.now()
        events = []
        if self.target_date < now and not self.final_state:
            self.final_state = True
            if self.status == self.STARTED or self.status == self.MISSED:
                self.status = self.MISSED
            else:
                events.append(self.OTHER_CONFIRMED)
#                 control.user_confirmed_a_state_update_in_another_user_s_mission(self.closed_by, self.get_absolute_url())
                if self.status == self.CLOSED:
                    if self.responsible == self.parent.owner:
                        events.append(self.DISCUSSION_OWNER_COMPLETED)
#                 control.user_confirmed_a_state_u
#                         control.user_completed_a_mission_for_his_own_s_discussion( self.responsible, self.get_absolute_url())
                    else:
                        events.append(self.OTHER_COMPLETED)
#                         control.user_completed_a_mission_for_another_user_s_discussion( self.responsible, self.get_absolute_url())
                else:
                    if self.status == self.ABORTED:
                        if self.responsible == self.parent.owner:
                            events.append(self.DISCUSSION_OWNER_ABORTED)
#                             control.user_aborted_a_mission_for_his_own_s_discussion( self.responsible, self.get_absolute_url())
                        else:
                            events.append(self.OTHER_ABORTED)
#                             control.user_aborted_a_mission_for_another_user_s_discussion( self.responsible, self.get_absolute_url())
                        
                                
            self.save()
            
        return events    
                    

    def get_status_obs(self):
        return self.status


    def print_content(self):
        print( 'create', self.created_at, 'update', self.updated_at, 'status:', self.get_status_display(), 'now', timezone.now(), 'GoalDescription:', self.goal_description, 'target_date:', self.target_date, 'remaining', self.get_time_until_target(), 'closing_date:', self.closed_at, self.status_description)
        
    def get_discussion(self):
        return self.parent


class Viewer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_counter = models.IntegerField(default = 0)
    views_counter_updated_at = models.DateTimeField(default=None, blank=True, null=True)
    discussion_updated_at_on_last_view = models.DateTimeField(default=None, blank=True, null=True)
    is_a_follower = models.BooleanField(default = False)
    is_invited    = models.BooleanField(default = False)

    
    def clear_views_counter(self):
        self.views_counter = 0
        self.save()
        
    def get_views_counter(self):
        return self.views_counter

    def start_follow_obs(self):
        self.is_a_follower = True
        self.save()


    def stop_follow_obs(self):
        self.is_a_follower = False
        self.save()

    def get_is_a_follower(self):
        return self.is_a_follower

    def invite_obs(self):
        self.is_invited = True
        self.save()

    def cancel_invitation_obs(self):
        self.is_invited = False
        self.save()

    def get_is_invited(self):
        return self.is_invited

    def print_content(self):
        print( 'user', self.user.username, 'views_counter', self.views_counter, 'updated_at', self.updated_at, 'views_counter_updated_at', self.views_counter_updated_at, 'is_a_follower', self.is_a_follower, 'is_invited', self.is_invited)
        for glimpse in self.glimpse_set.all().order_by("-created_at"):
            glimpse.print_content()
        

    def get_discussion(self):
        return self.discussion



class AnonymousVisitor(models.Model):
    user = models.ForeignKey(User, default = None,  null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.id)

    def print_content(self):
        if self.user:
            ident_string = self.user.username
        else:
            ident_string = None
        print( 'AnonymousVisitor', 'id', self.id, 'user', ident_string, 'updated_at', self.updated_at)
        



class AnonymousVisitorViewer(models.Model):
    anonymous_visitor = models.ForeignKey(AnonymousVisitor, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_counter = models.IntegerField(default = 0)
    views_counter_updated_at = models.DateTimeField(default=None, blank=True, null=True)
    discussion_updated_at_on_last_view = models.DateTimeField(default=None, blank=True, null=True)

    
    def increment_views_counter_obs(self):
        if self.discussion_updated_at_on_last_view != self.discussion.updated_at: 
            self.views_counter += 1            
            self.discussion_updated_at_on_last_view = self.discussion.updated_at
            glimpse = self.glimpse_set.create( anonymous_visitor_viewer = self)
            glimpse.clean()
            glimpse.save()            
            
            
        self.views_counter_updated_at = timezone.now()
        self.save()

    def clear_views_counter(self):
        self.views_counter = 0
        self.save()
        
    def get_views_counter(self):
        return self.views_counter
    
    def get_user(self):
        return self.anonymous_visitor.user
    
    def __str__(self):
        return "{} - {}: {}".format(self.id, self.views_counter, self.discussion.title)

    def print_content(self):
        if self.user:
            ident_string = self.user.username
        else:
            ident_string = None
        print( 'AnonymousVisitorViewer', 'id', self.id, 'user', ident_string, 'views_counter', self.views_counter, 'updated_at', self.updated_at, 'views_counter_updated_at', self.views_counter_updated_at, 'is_a_follower', self.is_a_follower, 'is_invited', self.is_invited)
        for glimpse in self.glimpse_set.all().order_by("-created_at"):
            glimpse.print_content()
            
    def get_discussion(self):
        return self.discussion
        

        
class Glimpse(models.Model):
    viewer = models.ForeignKey(Viewer, default = None,  null=True, blank=True, on_delete=models.CASCADE)
    anonymous_visitor_viewer = models.ForeignKey(AnonymousVisitorViewer, default = None,  null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return "{}: {}".format( self.created_at, self.id)

    def print_content(self):
        ident_string = ''
        discussion_title = ''
        if self.anonymous_visitor_viewer:
            ident_string = 'AnonymousVisitorViewer ' + int(self.id)
            discussion_title = self.anonymous_viewer.discussion.title
        if self.viewer:
            ident_string = self.viewer.user.username
            discussion_title = self.viewer.discussion.title
            
        print( 'at',  self.created_at, 'user', ident_string , 'looked at', discussion_title )
        
    def get_discussion(self):
        if self.viewer != None:
            return self.viewer.discussion
        return None


class FollowRelation(models.Model):
    follower_user = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='following_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('follower_user', 'following_user'),
        )

    def __str__(self):
        return "{} is following {}".format(self.follower_user.username, self.following_user.username)

    def print_content(self):
        print( self.follower_user.username , 'is following', self.following_user.username)

        
class Segment(models.Model):
    title = models.CharField(_(u"שם"), max_length=200)
    description = models.TextField(_(u"תאור"), blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.title, self.description)
    
    def is_in_segment(self, user):
        return user.userprofile in self.userprofile_set.all()
        
    def print_content(self):
        print( 'segment', self.title, ':', self.description)
        print( 'members are:')
        for user_profile in self.userprofile_set.all():
            print( user_profile.print_content())
         

class TaggedDiscussions(TaggedItemBase):
    content_object = models.ForeignKey('Discussion', on_delete=models.CASCADE)


class TaggedUsers(TaggedItemBase):
    content_object = models.ForeignKey('UserProfile', on_delete=models.CASCADE)


class KuterLessApp(models.Model):
    app_name                    = models.CharField(_("title"), max_length=200)
    app_description             = models.TextField( blank=True, null=True,
                                  validators=[MaxLengthValidator(MAX_TEXT)])
    email                       = models.EmailField(blank=True, null=True)
    created_at                  = models.DateTimeField(auto_now_add=True)
    updated_at                  = models.DateTimeField(auto_now=True)
       


class UserProfile(models.Model):
    user = models.OneToOneField(User, default = None, null=True, blank=True , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    segment = models.ForeignKey(Segment, null=True, blank=True, on_delete=models.CASCADE)
    recieve_notifications    = models.BooleanField(default = True)
    recieve_updates    = models.BooleanField(default = True)
    can_limit_discussion_access    = models.BooleanField(default = False)
    can_limit_discussion_to_login_users_only    = models.BooleanField(default = False)
    a_player    = models.BooleanField(default = False)
    location    = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    latitude    = models.FloatField(default=None, blank=True, null=True)
    longitude   = models.FloatField(default=None, blank=True, null=True)
#    recieve_personal_messages_from_users    = models.BooleanField(default = False)
    description = models.TextField(_("Description"), blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    location_desc = models.CharField( max_length=200,default=None, blank=True, null=True)
            
    followed_discussions_tags = TaggableManager( blank=True)
    
    application               = models.ForeignKey(KuterLessApp, null=True, blank=True, on_delete=models.CASCADE)
    application_specific_id   = models.IntegerField(blank=True, default = 0) #used when there is no email


    def __str__(self):
        return "{} ".format(self.user.username)
    
    def is_in_the_same_segment(self, another_user = None ):
        if another_user is None:
            if self.segment is None:
                return True
            return False
         
        if another_user not in User.objects.all():
            return False
        if not another_user.userprofile:
            return False
        
        return (self.segment == another_user.userprofile.segment)
    
    def set_segment(self, segment = None):
            
        self.segment = segment
        self.save()
        
    def get_segment(self):
            
        return self.segment

    def get_segment_title(self):
            
        if self.get_segment() :
            return self.segment.title
        return u'אתר הציבורי'


    def get_all_users_in_same_segment_list(self):
        all_users_in_same_segment_list = []
        for user in User.objects.all():
            if self.is_in_the_same_segment( user):
                all_users_in_same_segment_list.append(user)
                
        all_users_in_same_segment_list.remove(self.user)
                 
        return all_users_in_same_segment_list
    
    def print_content(self):
        print( self.user.username)
        if self.segment:
            print( 'belong to', self.segment.title)
        if self.segment:
            print( 'belong to segment', self.segment.title)
        else:
            print( 'belong to the default public segment')
            
        if self.recieve_notifications :
            print( 'recieve_notifications')
        if self.recieve_updates :
            print( 'recieve_updates')
        if self.can_limit_discussion_access :
            print( 'can_limit_discussion_access')
        if self.can_limit_discussion_to_login_users_only :
            print( 'can_limit_discussion_to_login_users_only')
        

class UserUpdate(models.Model):

    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion,  null=True, blank=True, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='applicabale_sender', null=True, blank=True, on_delete=models.CASCADE)
    header = models.CharField( max_length=200)
    content = models.TextField( blank=True, null=True,
                                   validators=[MaxLengthValidator(MAX_TEXT)])
    details_url = models.CharField( max_length=200,  blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    already_read    = models.BooleanField(default = False)

    def __str__(self):
        return self.header

    def can_user_access(self, viewing_user = None):
        if self.discussion:
            return self.discussion.can_user_access_discussion(viewing_user)
        if not self.recipient.userprofile.is_in_the_same_segment(viewing_user):
            return False
        
        if not self.recipient.userprofile.is_in_the_same_segment(viewing_user):
            return False
        
        if self.sender:
            if not self.sender.userprofile.is_in_the_same_segment(viewing_user):
                return False
            
        return True
    
    def set_as_already_read(self):
        self.already_read = True
        self.save()
        
    def set_as_unread(self):
        self.already_read = False
        self.save()
    
    def get_if_already_read(self):
        return self.already_read
    
    def get_if_long(self):
        if self.header.endswith('...'):
            return True
        return False
        
    
    def print_content(self):
        print( 'to:', self.recipient, 'head', self.header, 'content', self.content, 'from', self.sender, 'url', self.details_url)
        if self.discussion:
            self.discussion.print_content()

    def get_absolute_url(self):
        return (
        reverse('coplay:user_update_details', kwargs={'pk': str(self.id)}) )

    def get_discussion(self):
        return self.discussion
    
    
# class SaftyEnhancement(models.Model):
#     OPEN     = 1
#     FIXED    = 2
#     CANCELED = 3
#     
#     PROGRESS_STATUS = (
#         (OPEN    , u'נפתח'),
#         (FIXED   , u'תוקן'),
#         (CANCELED, u'בוטל'),
#     )
# 
#     kuterless_discussion         = models.ForeignKey(Discussion)
#     progress_status              = models.IntegerField(choices=PROGRESS_STATUS)
#     discus_id                    = models.IntegerField(blank=True, default = 0)
#     created_at                   = models.DateTimeField(auto_now_add=True)
#     updated_at                   = models.DateTimeField(auto_now=True)
#     
#     def __str__(self):
#         return self.id

    
