from coplay.models import Discussion
from django.contrib.auth.models import User
from django.test import TestCase


class CoPlayTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('User1', 'user1@example.com',
                                              'secret')

    def create_dicussion(self):
        d = Discussion()
        d.owner = self.user1
        d.title = "Visit the moon"
        d.full_clean()
        d.save()
        return d

    def test_create_discussion(self):
        self.assertEquals(0, Discussion.objects.count())
        d = self.create_dicussion()
        self.assertEquals(1, Discussion.objects.count())
