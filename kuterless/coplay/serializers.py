# -*- coding: utf-8 -*-

from coplay.models import Discussion
from rest_framework import serializers
from django.contrib.auth.models import User

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
                  'is_restricted'
                  )

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id',
                  'username'
                  )
        