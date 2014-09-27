# -*- coding: utf-8 -*-
from coplay import api
from coplay.models import UserProfile
from django.contrib.auth.models import User
from django.test import TestCase
from memecache.models import Account
from public_fulfillment.control import create_kuterless_user, simple_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.test import APIRequestFactory
from rest_framework.urlpatterns import format_suffix_patterns

class PublicFulfillmentTest(TestCase):

    def setUp(self):
        
        self.factory = APIRequestFactory()
        
    def create_user(self):
        
        self.user = create_kuterless_user('zugu', '1234', 'john', 'doo', 'ee@dd.com', False)

    
    def test_create_kuterless_user(self):
        self.assertEquals(0, User.objects.count())
        self.assertEquals(0, UserProfile.objects.count())
        self.assertEquals(0, Account.objects.count())
        self.assertEquals(0, Token.objects.count())
        
        self.create_user()

        self.assertEquals(1, User.objects.count())
        self.assertEquals(1, UserProfile.objects.count())
        self.assertEquals(1, Account.objects.count())
        self.assertEquals(1, Token.objects.count())


        self.assertEquals( 'zugu', self.user.username)
        self.assertEquals( True, self.user.check_password('1234'))
        self.assertEquals( 'john', self.user.first_name)
        self.assertEquals( 'doo', self.user.last_name)
        self.assertEquals(  'ee@dd.com', self.user.email)
        self.assertEquals(  self.user.userprofile.recieve_updates, False)

    def test_obtain_auth_token(self):
        
        self.create_user()

        
        print 'wrong authentication'
        request = self.factory.post('/api-token-auth/', {'username': self.user.username, 'password':'wrong password'}, format='json')
        response = obtain_auth_token(request)
        self.assertEquals(  response.data, {u'non_field_errors': [u'Unable to login with provided credentials.']})

        print 'correct authentication'
        request = self.factory.post('/api-token-auth/', {'username': self.user.username, 'password':'1234'}, format='json')
        print "this is the request:\n", request
        print "body:\n", request.body
        
        self.assertEquals(  request.body, '{"username": "zugu", "password": "1234"}')
        
        response = obtain_auth_token(request)
        print "response is\n", response.data
        
                
        self.assertEquals(  response.data, {'token': self.user.auth_token.key})
        print 'non authenticated get'
        request = self.factory.get('/labs/coplay/api/example_view/', format='json')
        response = api.example_view(request)
        print "response is\n", response.data
        found_user =  simple_auth_token(self.user.auth_token.key)
        self.assertEquals(  self.user, found_user)

        print 'authenticated get'
        request = self.factory.get('/labs/coplay/api/example_view/', format='json')
        request.user = self.user
        response = api.example_view(request)
        print "response is\n", response.data


        
        
        