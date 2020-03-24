from classytags.core import Tag
from models import *
from django.contrib import admin

# Register your models here.

class BusinessCardAdmin(admin.ModelAdmin):
    list_display = (
    'private_name'
    ,'family_name' 
    ,'email'
    ,'phone_number'
    ,'url',)


class AcquaintanceAdmin(admin.ModelAdmin):
    list_display = (
    'business_card',
    'id',)

admin.site.register(BusinessCard, BusinessCardAdmin)    
admin.site.register(Acquaintance, AcquaintanceAdmin)    
