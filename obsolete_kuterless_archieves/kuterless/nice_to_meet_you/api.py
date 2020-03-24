# -*- coding: utf-8 -*-
#from coplay.control import \
#    user_posted_a_feedback_in_another_other_user_s_discussion
#from coplay.models import Discussion, Feedback, Decision, Vote, Task, Viewer, \
#    AnonymousVisitor, AnonymousVisitorViewer, Glimpse, FollowRelation, UserProfile, \
#    UserUpdate
#from coplay.serializers import DiscussionSerializer, UserSerializer, \
#    FeedbackSerializer, DecisionSerializer, VoteSerializer, TaskSerializer, \
#    ViewerSerializer, AnonymousVisitorSerializer, AnonymousVisitorViewerSerializer, \
#    GlimpseSerializer, FollowRelationSerializer, UserProfileSerializer, \
#    UserUpdateSerializer, DiscussionWholeSerializer, DecisionWholeSerializer, \
#    AddFeedBackSerializer, AddTaskSerializer, AddDiscussionSerializer
#from coplay.services import discussion_add_feedback, discussion_add_task, \
#    can_user_acess_discussion, get_all_users_visiabale_for_a_user_list, \
#    is_in_the_same_segment, get_accessed_list, task_get_status, create_discussion
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
from serializers import MessageSerializer
from models import *


class MessagesList(APIView):
    def get(self, request,format = None):
#        serialized_messages = MessageSerializer(Acquaintance.objects.all().order_by("-updated_at").first(), request.user, many = False)
        serialized_messages = MessageSerializer(Acquaintance.objects.all().order_by("-updated_at"), request.user, many = True)
        return Response(serialized_messages.data)


