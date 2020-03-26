# -*- coding: utf-8 -*-
"""
This file contain the services, used for all views
"""
from coplay.control import init_user_profile, init_user_token
from django.contrib.auth.models import User
from memecache.control import init_user_account

def create_kuterless_user(  user_name, password, first_name = None, last_name = None, email = None, recieve_updates = True, description= None, location_desc = None, followed_discussions_tags = None, segment = None):
    
                
    if User.objects.filter( username = user_name ).count() != 0:        
        return None
    
    user = User(
            username=user_name,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    user.set_password(password)
    user.save()    
    init_user_profile(user, segment)
    init_user_account(user)
    init_user_token(user)
    user.userprofile.recieve_updates = recieve_updates
    user.userprofile.description = description
    user.userprofile.location_desc = location_desc
    user.userprofile.save()
    
    return user



    
