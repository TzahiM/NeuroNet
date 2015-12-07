# -*- coding: utf-8 -*-
from coplay.control import \
    user_posted_a_feedback_in_another_other_user_s_discussion
from coplay.models import Discussion, Feedback, Decision, Vote, Task, Viewer, \
    AnonymousVisitor, AnonymousVisitorViewer, Glimpse, FollowRelation, UserProfile, \
    UserUpdate
from coplay.serializers import DiscussionSerializer, UserSerializer, \
    FeedbackSerializer, DecisionSerializer, VoteSerializer, TaskSerializer, \
    ViewerSerializer, AnonymousVisitorSerializer, AnonymousVisitorViewerSerializer, \
    GlimpseSerializer, FollowRelationSerializer, UserProfileSerializer, \
    UserUpdateSerializer, DiscussionWholeSerializer, DecisionWholeSerializer, \
    AddFeedBackSerializer, AddTaskSerializer
from coplay.services import discussion_add_feedback, discussion_add_task, \
    can_user_acess_discussion, get_all_users_visiabale_for_a_user_list, \
    is_in_the_same_segment, get_accessed_list, task_get_status
from django.contrib.auth.models import User
from django.http.response import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import parsers, renderers
from rest_framework.authentication import SessionAuthentication, \
    TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


class DiscussionList(APIView):
    def get(self, request,format = None):
        
        serialized_discussions = DiscussionSerializer(get_accessed_list( Discussion.objects.all(), request.user), many = True)
        return Response(serialized_discussions.data)



class DiscussionDetails(APIView):
    def get_object(self, pk):
            try:
                return Discussion.objects.get(pk = pk)
            except Discussion.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        discussion = self.get_object(pk)
        if not can_user_acess_discussion(discussion, request.user):
            discussion = None
        serialized_discussion = DiscussionSerializer(discussion)
        return Response(serialized_discussion.data)


class UserList(APIView):
    def get(self, request,format = None):
        users = get_all_users_visiabale_for_a_user_list(request.user)
        serialized_users =UserSerializer(users, many = True)
        return Response(serialized_users.data)



class UserDetails(APIView):
    def get_object(self, pk):
            try:
                return User.objects.get(pk = pk)
            except User.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        serialized_user = None
        user = self.get_object(pk)
        if is_in_the_same_segment( request.user, user):
            serialized_user = UserSerializer(user)

        return Response(serialized_user.data)


class FeedbackList(APIView):
    def get(self, request,format = None):
        
        serialized_feedbacks =FeedbackSerializer(get_accessed_list( Feedback.objects.all(), request.user), many = True)
        return Response(serialized_feedbacks.data)



class FeedbackDetails(APIView):
    def get_object(self, pk):
            try:
                return Feedback.objects.get(pk = pk)
            except Feedback.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        feedback = self.get_object(pk)
        serialized_feedback = None
        if  can_user_acess_discussion(feedback.discussion, request.user):
            serialized_feedback = FeedbackSerializer(feedback)
        return Response(serialized_feedback.data)



class DecisionList(APIView):
    def get(self, request,format = None):
        
        serialized_decisions =DecisionSerializer(get_accessed_list( Decision.objects.all(), request.user), many = True)
        return Response(serialized_decisions.data)



class DecisionDetails(APIView):
    def get_object(self, pk):
            try:
                return Decision.objects.get(pk = pk)
            except Decision.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        decision = self.get_object(pk)
        if  not can_user_acess_discussion(decision.parent, request.user):
            decision = None
        serialized_decision = DecisionSerializer(decision)
        return Response(serialized_decision.data)


class VoteList(APIView):
    def get(self, request,format = None):

        serialized_votes =VoteSerializer(get_accessed_list( Vote.objects.all(), request.user), many = True)
        return Response(serialized_votes.data)



class VoteDetails(APIView):
    def get_object(self, pk):
            try:
                return Vote.objects.get(pk = pk)
            except Vote.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        vote = self.get_object(pk)
        
        if not can_user_acess_discussion( vote.get_discuaaion(), request.user):
            vote = None
        
        
        serialized_vote = VoteSerializer(vote)
        return Response(serialized_vote.data)


class TaskList(APIView):
    def get(self, request,format = None):
        not_missed_tasks = []
        tasks = Task.objects.all()
        for task in tasks:
            status =  task_get_status( task)
            if status != task.MISSED and can_user_acess_discussion(task.parent, request.user):
                not_missed_tasks.append(task)
        
        serialized_tasks =TaskSerializer(get_accessed_list( not_missed_tasks, request.user), many = True)
        return Response(serialized_tasks.data)



class TaskDetails(APIView):
    def get_object(self, pk):
        try:
            task = Task.objects.get(pk = pk)
            if task.get_status() != task.MISSED:
                return task
            raise Http404
        except Task.DoesNotExist:
            raise Http404
            
    def get(self, request, pk, format = None):
        task = self.get_object(pk)
        status =  task_get_status( task)
        if status == task.MISSED or ( False == can_user_acess_discussion(task.get_discussion(), request.user)):
            task = None

        serialized_task = TaskSerializer(task)
        return Response(serialized_task.data)


class ViewerList(APIView):
    def get(self, request,format = None):

        serialized_viewers =ViewerSerializer(get_accessed_list( Viewer.objects.all(), request.user), many = True)
        return Response(serialized_viewers.data)



class ViewerDetails(APIView):
    def get_object(self, pk):
            try:
                return Viewer.objects.get(pk = pk)
            except Viewer.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        viewer = self.get_object(pk)
        if not can_user_acess_discussion(viewer.get_discussion(), request.user):
            viewer = None
                
        serialized_viewer = ViewerSerializer(viewer)
        return Response(serialized_viewer.data)


class AnonymousVisitorList(APIView):
    def get(self, request,format = None):
        anonymousvisitors = AnonymousVisitor.objects.all()
        
        if request.user.is_authenticated() and request.user.user_profile.segment != None:
            anonymousvisitors = []
        
        serialized_anonymousvisitor =AnonymousVisitorSerializer(get_accessed_list( anonymousvisitors, request.user), many = True)
        return Response(serialized_anonymousvisitor.data)


class AnonymousVisitorDetails(APIView):
    def get_object(self, pk):
            try:
                return AnonymousVisitor.objects.get(pk = pk)
            except AnonymousVisitor.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        anonymousvisitor = self.get_object(pk)
        
        if request.user.is_authenticated() and request.user.user_profile.segment != None:
            anonymousvisitor = None
        else:       
            if not can_user_acess_discussion(anonymousvisitor.get_discussion(), request.user):
                anonymousvisitor = None

        
        serialized_anonymousvisitor = AnonymousVisitorSerializer(anonymousvisitor)
        return Response(serialized_anonymousvisitor.data)


class AnonymousVisitorViewerList(APIView):
    def get(self, request,format = None):
        anonymousvisitorvviewers = AnonymousVisitorViewer.objects.all()
        
        if request.user.is_authenticated() and request.user.user_profile.segment != None:
            anonymousvisitorvviewers = []
        
        serialized_anonymousvisitorvviewers =AnonymousVisitorViewerSerializer(get_accessed_list( anonymousvisitorvviewers, request.user), many = True)
        return Response(serialized_anonymousvisitorvviewers.data)



class AnonymousVisitorViewerDetails(APIView):
    def get_object(self, pk):
        try:
            return AnonymousVisitorViewer.objects.get(pk = pk)
        except AnonymousVisitorViewer.DoesNotExist:
            raise Http404
            
    def get(self, request, pk, format = None):
        anonymousvisitorvviewer = self.get_object(pk)
        
        if request.user.is_authenticated() and request.user.user_profile.segment != None:
            anonymousvisitorvviewer = None
        else:
            if not can_user_acess_discussion(anonymousvisitorvviewer.get_discussion(), request.user):
                anonymousvisitorvviewer = None
        
        
        
        serialized_anonymousvisitorvviewer = AnonymousVisitorViewerSerializer(anonymousvisitorvviewer)
        return Response(serialized_anonymousvisitorvviewer.data)


class GlimpseList(APIView):
    def get(self, request,format = None):
        glimpses = Glimpse.objects.all()
        
        if request.user.is_authenticated() and request.user.user_profile.segment != None:
            glimpses = []
        
        
        serialized_glimpses =GlimpseSerializer(get_accessed_list( glimpses, request.user), many = True)
        return Response(serialized_glimpses.data)



class GlimpseDetails(APIView):
    def get_object(self, pk):
        try:
            return Glimpse.objects.get(pk = pk)
        except Glimpse.DoesNotExist:
            raise Http404
            
    def get(self, request, pk, format = None):
        glimpse = self.get_object(pk)
        
        if not can_user_acess_discussion(glimpse.get_discussion(), request.user):
            glimpse = None
        
        
        serialized_glimpse = GlimpseSerializer(glimpse)
        return Response(serialized_glimpse.data)


class FollowRelationList(APIView):
    def get(self, request,format = None):
        followrelations = FollowRelation.objects.all()
        allowed_relations = []
        for folloewr_relation in followrelations:
            if is_in_the_same_segment( request.user, folloewr_relation.follower_user) and is_in_the_same_segment( request.user, folloewr_relation.following_user):
                allowed_relations.append(folloewr_relation)
        
        serialized_followrelations =FollowRelationSerializer(allowed_relations, many = True)
        return Response(serialized_followrelations.data)



class FollowRelationDetails(APIView):
    def get_object(self, pk):
            try:
                return FollowRelation.objects.get(pk = pk)
            except FollowRelation.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        followrelation = self.get_object(pk)
        if not (is_in_the_same_segment( request.user, followrelation.follower_user) and is_in_the_same_segment( request.user, followrelation.following_user)):
            followrelation = None
        serialized_followrelation = FollowRelationSerializer(followrelation)
        return Response(serialized_followrelation.data)


class UserProfileList(APIView):
    def get(self, request,format = None):
        userprofiles = UserProfile.objects.all()
        allowed_userprofiles = []
        for userprofile in userprofiles:
            if is_in_the_same_segment( request.user, userprofile.user):
                allowed_userprofiles.append(userprofile)
                
        serialized_userprofiles =UserProfileSerializer(allowed_userprofiles, many = True)
        return Response(serialized_userprofiles.data)



class UserProfileDetails(APIView):
    def get_object(self, pk):
            try:
                return UserProfile.objects.get(pk = pk)
            except UserProfile.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        userprofile = self.get_object(pk)
        if not is_in_the_same_segment( request.user, userprofile.user):
            userprofile = None
            
        serialized_userprofile = UserProfileSerializer(userprofile)
        return Response(serialized_userprofile.data)


class UserUpdateList(APIView):
    def get(self, request,format = None):
        userupdates = UserUpdate.objects.order_by("-created_at")
        allowed_userupdates = []
        for user_update in userupdates:
            if is_in_the_same_segment( request.user, user_update.recipient):
                allowed_userupdates.append(user_update)
            
        serialized_userupdates =UserUpdateSerializer(allowed_userupdates, many = True)
        return Response(serialized_userupdates.data)



class UserUpdateListUnRead(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,format = None):
        userupdates = UserUpdate.objects.filter(recipient = request.user, already_read = False).order_by("-created_at")

        serialized_userupdates =UserUpdateSerializer(userupdates, many = True)
        return Response(serialized_userupdates.data)


class UserUpdateDetails(APIView):
    def get_object(self, pk):
            try:
                return UserUpdate.objects.get(pk = pk)
            except UserUpdate.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        userupdate = self.get_object(pk)
        if not is_in_the_same_segment(request.user, userupdate.recipient):
            userupdate = None
            
        serialized_userupdate = UserUpdateSerializer(userupdate)
        return Response(serialized_userupdate.data)
    

@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def userupdate_read_notification(request, pk,format=None):
    try:
        user_update = UserUpdate.objects.get(pk = pk)
    except UserUpdate.DoesNotExist:
        return Response({'response': "user update not found"})
    if user_update.recipient != request.user:
        return Response({'response': "update does not belong to authenticated user"})
    
    user_update.set_as_already_read()
    
    return Response({'response': "OK"})

class DecisionWhole(APIView):
    def get_object(self, pk):
            try:
                return Decision.objects.get(pk = pk)
            except Decision.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        decision = self.get_object(pk)
        if  not can_user_acess_discussion(decision.parent, request.user):
            decision = None
        
        serialized_decision = DecisionWholeSerializer(decision)
        return Response(serialized_decision.data)

class DiscussionWhole(APIView):
    def get_object(self, pk):
            try:
                return Discussion.objects.get(pk = pk)
            except Discussion.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        discussion = self.get_object(pk)
        not_missed_tasks = []
        if can_user_acess_discussion( discussion, request.user):            
            for task in discussion.task_set.all():
                if task_get_status(task) != task.MISSED:
                    not_missed_tasks.append(task)
        else:
            discussion = None
                
        serialized_discussion = DiscussionWholeSerializer(discussion)
        return Response(serialized_discussion.data)


        
@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    
    return Response(content)


class AddFeedBackView(APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    
    def dispatch(self, *args, **kwargs):
        return super(AddFeedBackView, self).dispatch(*args, **kwargs)
        
    def get_object(self, pk):
            try:
                return Discussion.objects.get(pk = pk)
            except Discussion.DoesNotExist:
                raise Http404
            

    def post(self, request, pk, format = None,csrf_exempt = True):
        discussion = self.get_object(pk)
        created_feedback_serializer = AddFeedBackSerializer(data=request.DATA)        
        
        if not created_feedback_serializer.is_valid():
            return Response(created_feedback_serializer.errors)

        feedback, error_string = discussion_add_feedback( discussion, 
                                                          request.user,feedbabk_type = created_feedback_serializer.object.feedback_type, 
                                                          content = created_feedback_serializer.object.content)
        if feedback:
            serialized_feedback = FeedbackSerializer(feedback)
            return Response(serialized_feedback.data)
            
        return Response({'response': error_string})


class AddTaskView(APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    
    def dispatch(self, *args, **kwargs):
        return super(AddTaskView, self).dispatch(*args, **kwargs)
        
    def get_object(self, pk):
            try:
                return Discussion.objects.get(pk = pk)
            except Discussion.DoesNotExist:
                raise Http404
            

    def post(self, request, pk, format = None,csrf_exempt = True):
        discussion = self.get_object(pk)
        created_task_serializer = AddTaskSerializer(data=request.DATA)        
        
        if not created_task_serializer.is_valid():
            return Response(created_task_serializer.errors)
        task, error_string = discussion_add_task(discussion, 
                                                 request.user, 
                                                 created_task_serializer.object.goal_description, 
                                                 created_task_serializer.object.target_date)
        if task:
            serialized_task = TaskSerializer(task)
        
            return Response(serialized_task.data)

        return Response({'response': error_string})

# class AddDiscussionView(APIView):
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     renderer_classes = (renderers.JSONRenderer,)
#      
#      
#     def dispatch(self, *args, **kwargs):
#         return super(AddDiscussionView, self).dispatch(*args, **kwargs)
#          
#     def get_object(self, pk):
#             try:
#                 return Discussion.objects.get(pk = pk)
#             except Discussion.DoesNotExist:
#                 raise Http404
#              
#  
#     def post(self, request, pk, format = None,csrf_exempt = True):
#         discussion = self.get_object(pk)
#         created_task_serializer = AddTDiscussionSerializer(data=request.DATA)        
#          
#         if not created_task_serializer.is_valid():
#             return Response(created_task_serializer.errors)
#         task, error_string = discussion_add_task(discussion, 
#                                                  request.user, 
#                                                  created_task_serializer.object.goal_description, 
#                                                  created_task_serializer.object.target_date)
#         if task:
#             serialized_task = TaskSerializer(task)
#          
#             return Response(serialized_task.data)
#  
#         return Response({'response': error_string})

@csrf_exempt
def create_feedback_view(request,pk):
    return AddFeedBackView.as_view()(request,pk)

@csrf_exempt
def create_task_view(request,pk):
    return AddTaskView.as_view()(request,pk)

# @csrf_exempt
# def create_discussion_view(request,pk):
#     return AddDiscussionView.as_view()(request,pk)
