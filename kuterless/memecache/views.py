# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from coplay.control import post_update_to_user
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task, \
    Viewer, FollowRelation, UserUpdate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
import floppyforms as forms

# Create your views here.

def shop_details(request, pk):
    return HttpResponse('shop_details ' + int(pk))
def product_details(request, pk):
    return HttpResponse('product_details ' + int(pk))
def cart_details(request, pk):
    return HttpResponse('cart_details ' + int(pk))
def account_details(request, pk):
    return HttpResponse('account_details ' + int(pk))
def transaction_details(request, pk):
    return HttpResponse('transaction_details ' + int(pk))
def purchase_details(request, pk):
    return HttpResponse('purchase_details ' + int(pk))
def item_voucher_details(request, pk):
    return HttpResponse('item_voucher_details ' + int(pk))

"""
memcache Ooosh
product list
product create
product update
product details
product selection
cart
my coupons
coupon details





"""
