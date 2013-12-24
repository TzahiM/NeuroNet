from CoPlay.models import Discussion, Response, Action, Vote, \
    Decision
from django.contrib import admin

# Register your models here.

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Owner', 'create_date')
    ordering = ['create_date']
    search_fields = ['Title',  'Owner']
    
class ResponseAdmin(admin.ModelAdmin):
    list_display = ( 'ResponseType', 'create_date')
    ordering = ['ResponseType', 'create_date']
    search_fields = ['ResponseType']


class ActionAdmin(admin.ModelAdmin):
    list_display = ( 'responsible', 'GoalDescription')

class VoteAdmin(admin.ModelAdmin):
    list_display = ( 'Voater', 'Value')

class DecisionAdmin(admin.ModelAdmin):
    list_display = ( 'TextBody','create_date')



admin.site.register(Response, ResponseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Discussion, DiscussionAdmin)

