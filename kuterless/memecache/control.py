# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""
from coplay.models import UserProfile, Discussion, UserUpdate
from django.contrib.auth.models import User
from memecache.models import Account


def init_user_account(user):
    user.account = Account(user = user)
    user.account.save()
    user.save()    
    
