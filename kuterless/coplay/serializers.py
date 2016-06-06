# -*- coding: utf-8 -*-

from coplay import models
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task, \
    Viewer, FollowRelation, UserUpdate, Vote, Glimpse, AnonymousVisitor, \
    AnonymousVisitorViewer, UserProfile, MAX_TEXT
from coplay.services import MAX_MESSAGE_INPUT_CHARS
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
                  'description_updated_at',
                  'is_restricted',
                  'is_viewing_require_login',
                  'latitude',
                  'longitude',
                  'location_desc',
                  'parent_url',
                  'parent_url_text',
                  'movie_url',
                  'movie_url_url_text',
                  'picture',
                  'anyway_progress_status',
                  'anyway_discuss_id',
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
                    'a_player',
                    'longitude',
                    'latitude',
                    'location_desc',
                    'description'
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
                  'latitude',
                  'longitude',
                  'location_desc',                  
                  'parent_url',
                  'parent_url_text',
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


class CreateTask(object):
    
    def __init__(self, goal_description, target_date):
        self.goal_description = goal_description
        self.target_date = target_date

class CreateDiscussion(object):
    
    def __init__(self,  title          ,
                        description    ,
                        location_desc  = None ,
                        tags_string    = None ,
                        parent_url     = None ,
                        parent_url_text= None ,
                        latitude       = None ,
                        longitude      = None ,
                        picture                = None ,
                        anyway_progress_status = None ,
                        anyway_discuss_id      = None ,
                        movie_url              = None ,
                        movie_url_url_text     = None ):

        self.title           = title          
        self.description     = description    
        self.location_desc   = location_desc  
        self.tags_string     = tags_string           
        self.parent_url      = parent_url     
        self.parent_url_text = parent_url_text
        self.latitude        = latitude       
        self.longitude       = longitude      
        self.picture                      = picture                     
        self.anyway_progress_status       = anyway_progress_status      
        self.anyway_discuss_id            = anyway_discuss_id           
        self.movie_url                    = movie_url                   
        self.movie_url_url_text           = movie_url_url_text          

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
    
class AddTaskSerializer(serializers.Serializer):
    goal_description = serializers.CharField(max_length = MAX_TEXT)
    target_date =  serializers.DateTimeField()

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.goal_description = attrs.get('goal_description', instance.goal_description)
            instance.target_date = attrs.get('target_date', instance.target_date)
            return instance
                
        return CreateTask( **attrs)

class AddDiscussionSerializer(serializers.Serializer):
    title                   = serializers.CharField(max_length = 200, required = True)
    description             = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = True)    
    location_desc           = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
    parent_url              = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
    parent_url_text         = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
    latitude                = serializers.FloatField( required = False)
    longitude               = serializers.FloatField( required = False) 
    tags_string             = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
    picture                 = serializers.ImageField( allow_empty_file = True, required =False,default = None,max_length = 50000)
    movie_url               = serializers.URLField( max_length=MAX_TEXT,default=None, required=False )                                                   
    movie_url_url_text      = serializers.CharField( max_length=MAX_TEXT,default=None, required=False)
    anyway_progress_status  = serializers.IntegerField(default=None, required = False)
    anyway_discuss_id       = serializers.IntegerField(default=None, required = False)
    
    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.title                  = attrs.get('title'           , instance.title           )
            instance.description            = attrs.get('description'     , instance.description     )
            instance.location_desc          = attrs.get('location_desc'   , instance.location_desc   )
            instance.tags_string            = attrs.get('tags_string'     , instance.tags_string     )
            instance.parent_url             = attrs.get('parent_url'      , instance.parent_url      )
            instance.parent_url_text        = attrs.get('parent_url_text' , instance.parent_url_text )
            instance.latitude               = attrs.get('latitude'        , instance.latitude        )
            instance.longitude              = attrs.get('longitude'       , instance.longitude       )
            instance.email                  = attrs.get('email'                        , instance.email                        )
            instance.picture                = attrs.get('picture'                      , instance.picture                      )
            instance.anyway_progress_status = attrs.get('anyway_progress_status'       , instance.anyway_progress_status       )
            instance.anyway_discuss_id      = attrs.get('anyway_discuss_id '           , instance.anyway_discuss_id            )
            instance.movie_url              = attrs.get('movie_url'                    , instance.movie_url                    )
            instance.movie_url_url_text     = attrs.get('movie_url_url_text'           , instance.movie_url_url_text           )
            instance.anyway_progress_status = attrs.get('anyway_progress_status'       , instance.anyway_progress_status       )
            instance.anyway_discuss_id      = attrs.get('anyway_discuss_id'            , instance.anyway_discuss_id            )
            return instance
                
        return CreateDiscussion( **attrs)
    

    
# class AddSaftyEnhancementSerializer(serializers.Serializer):
# #     ENCOURAGE = 1
# #     COOPERATION = 2
# #     INTUITION   = 3
# #     ADVICE      = 4
# 
# #     ENHANSMENT_TYPES = (
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #         (, ''),
# #     )
# #     
# # מעגל תנועה
# # גדר בטיחות
# # תאונת דרכים
# # מניעת תאונות
# # צומת
# # זכות קדימה
# # תמרור
# # מעבר חציה
# # מהירות נסיעה
# # רמזור
# # שוליים
# # התהפכות
# # גשר
# # מנהרה
# # הפרדה מפלסית
# # פס האטה
# # מדרכה
# # רחוב מגורים
# # אזור ילדים
# # בית ספר
# # מתנס
# # מרכז פעילות לקשישים
# # עומס תנועה
# # כביש עוקף
# # אבני שפה
# # קו הפרדה
# # מחלף
# # רמפה
#     enhansment_type = serializers.ChoiceField( choices = ENHANSMENT_TYPES, required        = False)
#     location_desc   = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
#     latitude        = serializers.FloatField( required = False)
#     longitude       = serializers.FloatField( required = False) 
#     description     = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)  
#     email           = serializers.EmailField( required = False); 
#     picture         = serializers.ImageField();
#     
#     
#     
#     
#     
#     
#     title           = serializers.CharField(max_length = 200)
#     description     = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS)    
#     location_desc   = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
#     tags            = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
#     parent_url      = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
#     parent_url_text = serializers.CharField(max_length = MAX_MESSAGE_INPUT_CHARS, required = False)
#     latitude        = serializers.FloatField( required = False)
#     longitude       = serializers.FloatField( required = False) 
# 
#     def restore_object(self, attrs, instance=None):
#         """
#         Given a dictionary of deserialized field values, either update
#         an existing model instance, or create a new model instance.
#         """
#         if instance is not None:
#             instance.title                 = attrs.get('title'           , instance.title           )
#             instance.description           = attrs.get('description'     , instance.description     )
#             instance.location_desc         = attrs.get('location_desc'   , instance.location_desc   )
#             instance.tags                  = attrs.get('tags'            , instance.tags            )
#             instance.parent_url            = attrs.get('parent_url'      , instance.parent_url      )
#             instance.parent_url_text       = attrs.get('parent_url_text' , instance.parent_url_text )
#             instance.latitude              = attrs.get('latitude'        , instance.latitude        )
#             instance.longitude             = attrs.get('longitude'       , instance.longitude       )
#             return instance
#                 
#         return CreateDiscussion( **attrs)
    
