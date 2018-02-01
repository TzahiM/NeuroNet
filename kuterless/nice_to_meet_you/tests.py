# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.serializers import json
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.test import APIRequestFactory, force_authenticate
import datetime
import time




class RedirectTest(TestCase):
    def setUp(self):
        return True



