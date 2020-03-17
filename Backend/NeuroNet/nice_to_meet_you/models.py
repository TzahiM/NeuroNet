# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from .control import update_vcf_file, update_sound_to_play_file, get_buisness_qr_code_image_name


class BusinessCard(models.Model):
    private_name = models.CharField(max_length=200, default=u'')
    family_name  = models.CharField(max_length=200, default=u'')
    email        = models.EmailField(max_length=70, blank=True)
    phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length= 17, default=u'') # validators should be a list    mobile_phone = models.CharField(max_length=200, default=u'')
    url          = models.URLField(max_length=2000, default=u'http://kuterless.org.il', blank=True)
    score    = models.PositiveIntegerField(default = 0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # ... other things not important here
        self.private_name = self.private_name.strip()  # Hopefully reduces junk to ""
        self.family_name  = self.family_name.strip()   # Hopefully reduces junk to ""
        self.url          = self.url.strip()           # Hopefully reduces junk to ""
        self.email        = self.email.lower().strip()        # Hopefully reduces junk to ""
        super(BusinessCard, self).save(*args, **kwargs)
        update_vcf_file( self.id, self.private_name,self.family_name,self.email, self.phone_number,self.url)
    
    def get_qr_code_url(self):
        return get_buisness_qr_code_image_name(self.id)
        
    def __str__(self):
        return self.private_name + self.family_name + str(self.id)


class Acquaintance(models.Model):
    business_card = models.ForeignKey(BusinessCard, on_delete=models.CASCADE)
    
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)
    message            = models.CharField(max_length=2000, default=u'')
    is_played          = models.BooleanField(default=False)

    
    def save(self, *args, **kwargs):
        super(Acquaintance, self).save(*args, **kwargs)
        update_sound_to_play_file( self.id, self.message)
        
    def __str__(self):
        return 'meeting ' + str(self.id) + ' of ' + str(self.business_card.id)
    
            
