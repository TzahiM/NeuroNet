# -*- coding: utf-8 -*-
from coplay.models import Discussion
from coplay.serializers import DiscussionSerializer, UserSerializer
from django.contrib.auth.models import User
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.views import APIView


class DiscussionList(APIView):
    def get(self, request,format = None):
        discussions = Discussion.objects.filter()
        serialized_discussions = DiscussionSerializer(discussions, many = True)
        return Response(serialized_discussions.data)



class DiscussionDetail(APIView):
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
        users = User.objects.filter()
        serialized_users =UserSerializer(users, many = True)
        return Response(serialized_users.data)



class UserDetail(APIView):
    def get_object(self, pk):
            try:
                return User.objects.get(pk = pk)
            except User.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        users = self.get_object(pk)
        serialized_user = UserSerializer(users)
        return Response(serialized_user.data)
        
