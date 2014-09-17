# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""
from memecache.models import Account, Shop, Product

def get_shop( user, pk):
    try:
        shop = Shop.objects.get(segment = user.userprofile.segment, id = int(pk))
    except Shop.DoesNotExist:
        return None
    
    return shop
    

def get_product( user, pk):
    try:
        product = Product.objects.get(id = int(pk))
    except Shop.DoesNotExist:
        return None
    
    if product.shop.segment == user.userprofile.segment:
        return product
    
    return None


def init_user_account(user):
    user.account = Account(user = user)
    user.account.save()
    user.save()    
    
