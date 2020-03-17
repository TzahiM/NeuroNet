# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User


def simple_auth_token( key):
    if key is None:
        return None
    
    for user in User.objects.all():
        if user.auth_token.key == key:
            return user        
    return None
        
    



