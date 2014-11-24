# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

#from coplay.models import UserProfile, Discussion, UserUpdate
from coplay.control import init_user_profile
from django.contrib.auth.models import User
from memecache.control import init_user_account
import models
from rest_framework.authtoken.models import Token


def init_user_token(user):
    Token.objects.get_or_create(user=user)


def create_kuterless_user(  user_name, password, first_name = None, last_name = None, email = None, recieve_updates = True, description= None, location_desc = None):
    
                
    if User.objects.filter( username = user_name ).exists():
        
        return None
    
    user = User(
            username=user_name,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    user.set_password(password)
    user.save()    
    init_user_profile(user)
    init_user_account(user)
    init_user_token(user)
    user.userprofile.recieve_updates = recieve_updates
    user.userprofile.description = description
    user.userprofile.location_desc = location_desc
    user.userprofile.save()
    
    return user


def simple_auth_token( key):
    if key is None:
        return None
    
    for user in User.objects.all():
        if user.auth_token.key == key:
            return user        
    return None
        
    


    