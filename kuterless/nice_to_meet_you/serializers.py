# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework import serializers
from models import *



class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Acquaintance
        fields = ('id',
                  'created_at',
                  'updated_at',
                  'message',
                  'is_played',
                  )

