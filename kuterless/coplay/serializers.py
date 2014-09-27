# -*- coding: utf-8 -*-

from coplay import models
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task, \
    Viewer, FollowRelation, UserUpdate, Vote, Glimpse, AnonymousVisitor, \
    AnonymousVisitorViewer, UserProfile, MAX_TEXT
from django.contrib.auth.models import User
from rest_framework import serializers



class DiscussionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Discussion
        fields = ('id',
                  'owner',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'locked_at',
                  'is_restricted',
                  'is_viewing_require_login'
                  )

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name'
                  )

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = ( 'id',
                   'discussion',
                    'user',
                    'feedbabk_type',
                    'content',
                    'created_at',
                    'updated_at'
                    )


class DecisionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Decision
        fields = ( 'id',
                   'parent',
                    'content',
                    'created_at',
                    'updated_at',
                    'value'
                    )
        


class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vote
        fields = ( 'id',
                   'voater',
                    'decision',
                    'created_at',
                    'updated_at',
                    'value',
                    )
        


class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ( 'id',
                   'parent',
                    'responsible',
                    'goal_description',
                    'target_date',
                    'closed_at',
                    'closed_by',
                    'status_description',
                    'status',
                    'created_at',
                    'updated_at',
                    'final_state'
                    )

 

class ViewerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Viewer
        fields = ( 'id',
                   'user',
                    'discussion',
                    'created_at',
                    'updated_at',
                    'views_counter',
                    'views_counter_updated_at',
                    'discussion_updated_at_on_last_view',
                    'is_a_follower',
                    'is_invited'
                    )
        


class GlimpseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Glimpse
        fields = ( 'id',
                   'viewer',
                    'anonymous_visitor_viewer',
                    'created_at',
                    'updated_at'
                    )



class AnonymousVisitorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnonymousVisitor
        fields = ( 'id',
                   'user',
                    'created_at',
                    'updated_at'
                    )



class AnonymousVisitorViewerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnonymousVisitorViewer
        fields = ( 'id',
                   'anonymous_visitor',
                   'discussion',
                    'created_at',
                    'updated_at',
                    'views_counter',
                    'views_counter_updated_at',
                    'discussion_updated_at_on_last_view'
                    )


class FollowRelationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FollowRelation
        fields = ( 'id',
                   'follower_user',
                   'following_user',
                    'created_at',
                    'updated_at'
                    )



class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ( 'id',
                   'user',
                    'created_at',
                    'updated_at',
                    'segment',
                    'recieve_notifications',
                    'recieve_updates',
                    'can_limit_discussion_access',
                    'can_limit_discussion_to_login_users_only',
                    'a_player'                    
                    )


class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserUpdate
        fields = ( 'id',
                   'recipient',
                    'discussion',
                    'sender',
                    'header',
                    'content',
                    'details_url',
                    'created_at',
                    'updated_at',
                    'already_read'
                    )

class DecisionWholeSerializer(serializers.ModelSerializer):
    
    vote_set = VoteSerializer(many=True)
    
    class Meta:
        model = Decision
        fields = ( 'id',
                   'parent',
                    'content',
                    'created_at',
                    'updated_at',
                    'value',
                    'vote_set'
                  )
        

class DiscussionWholeSerializer(serializers.ModelSerializer):
    
    feedback_set = FeedbackSerializer(many=True)
    task_set = TaskSerializer(many=True)
    decision_set = DecisionWholeSerializer( many = True)
    viewer_set = ViewerSerializer(many = True)
    
    class Meta:
        model = Discussion
        fields = ('id',
                  'owner',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'locked_at',
                  'is_restricted',
                  'is_viewing_require_login',
                  'feedback_set',
                  'task_set',
                  'decision_set',
                  'viewer_set'
                  )
        


class CreateFeedback(object):
    ENCOURAGE = 1
    COOPERATION = 2
    INTUITION = 3
    ADVICE = 4

    FEEDBACK_TYPES = (
        (ENCOURAGE, 'encourage'),
        (COOPERATION, 'cooporation'),
        (INTUITION, 'intuition'),
        (ADVICE, 'advice'),
    )
    
    def __init__(self, feedback_type, content):
        self.feedback_type = feedback_type
        self.content = content
 

class AddFeedBackSerializer(serializers.Serializer):
        
    feedback_type = serializers.ChoiceField(choices=CreateFeedback.FEEDBACK_TYPES)
    
    content = serializers.CharField(max_length=MAX_TEXT, min_length=None)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.feedback_type = attrs.get('feedback_type', instance.feedback_type)
            instance.content = attrs.get('content', instance.content)
            return instance
        
        return CreateFeedback(**attrs)
    
