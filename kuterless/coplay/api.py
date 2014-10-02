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
    AddFeedBackSerializer
from coplay.views import discussion_email_updates
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.signing import loads
from django.http.response import Http404
from django.template.base import Template
from django.template.context import Context
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, parsers, renderers
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication, TokenAuthentication
from rest_framework.compat import StringIO
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView



class DiscussionList(APIView):
    def get(self, request,format = None):
        discussions = Discussion.objects.all()
        serialized_discussions = DiscussionSerializer(discussions, many = True)
        return Response(serialized_discussions.data)



class DiscussionDetails(APIView):
    def get_object(self, pk):
            try:
                return Discussion.objects.get(pk = pk)
            except Discussion.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        discussion = self.get_object(pk)
        serialized_discussion = DiscussionSerializer(discussion)
        return Response(serialized_discussion.data)


class UserList(APIView):
    def get(self, request,format = None):
        users = User.objects.all()
        serialized_users =UserSerializer(users, many = True)
        return Response(serialized_users.data)



class UserDetails(APIView):
    def get_object(self, pk):
            try:
                return User.objects.get(pk = pk)
            except User.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        user = self.get_object(pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)




class FeedbackList(APIView):
    def get(self, request,format = None):
        feedbacks = Feedback.objects.all()
        serialized_feedbacks =FeedbackSerializer(feedbacks, many = True)
        return Response(serialized_feedbacks.data)



class FeedbackDetails(APIView):
    def get_object(self, pk):
            try:
                return Feedback.objects.get(pk = pk)
            except Feedback.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        feedback = self.get_object(pk)
        serialized_feedback = FeedbackSerializer(feedback)
        return Response(serialized_feedback.data)



class DecisionList(APIView):
    def get(self, request,format = None):
        decisions = Decision.objects.all()
        serialized_decisions =DecisionSerializer(decisions, many = True)
        return Response(serialized_decisions.data)



class DecisionDetails(APIView):
    def get_object(self, pk):
            try:
                return Decision.objects.get(pk = pk)
            except Decision.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        decision = self.get_object(pk)
        serialized_decision = DecisionSerializer(decision)
        return Response(serialized_decision.data)


class VoteList(APIView):
    def get(self, request,format = None):
        votes = Vote.objects.all()
        serialized_votes =VoteSerializer(votes, many = True)
        return Response(serialized_votes.data)



class VoteDetails(APIView):
    def get_object(self, pk):
            try:
                return Vote.objects.get(pk = pk)
            except Vote.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        vote = self.get_object(pk)
        serialized_vote = VoteSerializer(vote)
        return Response(serialized_vote.data)


class TaskList(APIView):
    def get(self, request,format = None):
        tasks = Task.objects.all()
        for task in tasks:
            task.refresh_status()
        serialized_tasks =TaskSerializer(tasks, many = True)
        return Response(serialized_tasks.data)



class TaskDetails(APIView):
    def get_object(self, pk):
            try:
                return Task.objects.get(pk = pk)
            except Task.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        task = self.get_object(pk)
        task.refresh_status()
        serialized_task = TaskSerializer(task)
        return Response(serialized_task.data)


class ViewerList(APIView):
    def get(self, request,format = None):
        viewers = Viewer.objects.all()
        serialized_viewers =ViewerSerializer(viewers, many = True)
        return Response(serialized_viewers.data)



class ViewerDetails(APIView):
    def get_object(self, pk):
            try:
                return Viewer.objects.get(pk = pk)
            except Viewer.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        viewer = self.get_object(pk)
        serialized_viewer = ViewerSerializer(viewer)
        return Response(serialized_viewer.data)


class AnonymousVisitorList(APIView):
    def get(self, request,format = None):
        anonymousvisitors = AnonymousVisitor.objects.all()
        serialized_anonymousvisitor =AnonymousVisitorSerializer(anonymousvisitors, many = True)
        return Response(serialized_anonymousvisitor.data)



class AnonymousVisitorDetails(APIView):
    def get_object(self, pk):
            try:
                return AnonymousVisitor.objects.get(pk = pk)
            except AnonymousVisitor.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        anonymousvisitor = self.get_object(pk)
        serialized_anonymousvisitor = AnonymousVisitorSerializer(anonymousvisitor)
        return Response(serialized_anonymousvisitor.data)


class AnonymousVisitorViewerList(APIView):
    def get(self, request,format = None):
        anonymousvisitorvviewers = AnonymousVisitorViewer.objects.all()
        serialized_anonymousvisitorvviewers =AnonymousVisitorViewerSerializer(anonymousvisitorvviewers, many = True)
        return Response(serialized_anonymousvisitorvviewers.data)



class AnonymousVisitorViewerDetails(APIView):
    def get_object(self, pk):
            try:
                return AnonymousVisitorViewer.objects.get(pk = pk)
            except AnonymousVisitorViewer.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        anonymousvisitorvviewer = self.get_object(pk)
        serialized_anonymousvisitorvviewer = AnonymousVisitorViewerSerializer(anonymousvisitorvviewer)
        return Response(serialized_anonymousvisitorvviewer.data)


class GlimpseList(APIView):
    def get(self, request,format = None):
        glimpses = Glimpse.objects.all()
        serialized_glimpses =GlimpseSerializer(glimpses, many = True)
        return Response(serialized_glimpses.data)



class GlimpseDetails(APIView):
    def get_object(self, pk):
            try:
                return Glimpse.objects.get(pk = pk)
            except Glimpse.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        glimpse = self.get_object(pk)
        serialized_glimpse = GlimpseSerializer(glimpse)
        return Response(serialized_glimpse.data)


class FollowRelationList(APIView):
    def get(self, request,format = None):
        followrelations = FollowRelation.objects.all()
        serialized_followrelations =FollowRelationSerializer(followrelations, many = True)
        return Response(serialized_followrelations.data)



class FollowRelationDetails(APIView):
    def get_object(self, pk):
            try:
                return FollowRelation.objects.get(pk = pk)
            except FollowRelation.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        followrelation = self.get_object(pk)
        serialized_followrelation = FollowRelationSerializer(followrelation)
        return Response(serialized_followrelation.data)


class UserProfileList(APIView):
    def get(self, request,format = None):
        userprofiles = UserProfile.objects.all()
        serialized_userprofiles =UserProfileSerializer(userprofiles, many = True)
        return Response(serialized_userprofiles.data)



class UserProfileDetails(APIView):
    def get_object(self, pk):
            try:
                return UserProfile.objects.get(pk = pk)
            except UserProfile.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        userprofile = self.get_object(pk)
        serialized_userprofile = UserProfileSerializer(userprofile)
        return Response(serialized_userprofile.data)


class UserUpdateList(APIView):
    def get(self, request,format = None):
        userupdates = UserUpdate.objects.order_by("-created_at")
        serialized_userupdates =UserUpdateSerializer(userupdates, many = True)
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
        for task in discussion.task_set.all():
            task.refresh_status()
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
#        if not discussion.can_user_access_discussion():
#            return Response(status=HTTP_401_UNAUTHORIZED )
    
#        data = JSONParser().parse(StringIO(request.body))
#        data = JSONParser().parse(request.body)
#        created_feedback_serializer = AddFeedBackSerializer(data=data)
#        created_feedback_serializer = AddFeedBackSerializer(data={"content": "sssss","feedback_type":1})
        
#         data1={"content": "sssss","feedback_type":1}
#         print 'ok'
#         print data1
#         data1=request.body
#         print 'data=request.body'
#         print data1
#         print 'request.POST'
#         print request.POST
#         print 'request.body'
#         print request.body
        
#        created_feedback_serializer = AddFeedBackSerializer(data=request.body)
#         stream = StringIO(request.body)
#         data = JSONParser().parse(stream)
#        print 'request'        
#         print 'request.DATA'
#         print request.DATA
#         print request.META['HTTP_AUTHORIZATION']
        created_feedback_serializer = AddFeedBackSerializer(data=request.DATA)        
#         print created_feedback_serializer.errors
#         print created_feedback_serializer.is_valid()
        
        
        if not created_feedback_serializer.is_valid():
#             print 'created_feedback_serializer.errors'
#            print created_feedback_serializer.errors
            return Response(created_feedback_serializer.errors)
#         print created_feedback_serializer.object.feedback_type
#         print created_feedback_serializer.object.content
#         print request.user
        if(request.user != discussion.owner and discussion.can_user_access_discussion(request.user) and discussion.is_active()):
            feedback = discussion.add_feedback(request.user, created_feedback_serializer.object.feedback_type, created_feedback_serializer.object.content)         
            serialized_feedback = FeedbackSerializer(feedback)     
            discussion.save() #verify that the entire discussion is considered updated
    
            t = Template("""
            {{feedbabk.user.get_full_name|default:feedbabk.user.username}} פירסם/ה {{feedbabk.get_feedbabk_type_name}}:\n
            "{{feedbabk.content}} "\n
            """)
    
            trunkated_subject_and_detailes = t.render(Context({"feedbabk": feedback}))
            
                                                                
                                                                
            discussion_email_updates(discussion,
                                             trunkated_subject_and_detailes,
                                             self.request.user,
                                             trunkated_subject_and_detailes)            
            discussion.start_follow(request.user)            
            user_posted_a_feedback_in_another_other_user_s_discussion(request.user, feedback.get_absolute_url())
#             print 'serialized_feedback.data'
#             print serialized_feedback.data                        
            return Response(serialized_feedback.data)
        
        return Response(status=HTTP_400_BAD_REQUEST)

@csrf_exempt
def create_feedback_view(request,pk):
    return AddFeedBackView.as_view()(request,pk)
