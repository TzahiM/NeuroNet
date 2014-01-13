from coplay.models import Feedback, Task, Decision, Vote, Discussion
from django.contrib import admin

# Register your models here.

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ( 'feedbabk_type', 'created_at')
    ordering = ['feedbabk_type', 'created_at']
    search_fields = ['feedbabk_type']


class TaskAdmin(admin.ModelAdmin):
    list_display = ( 'responsible', 'goal_description')

class VoteAdmin(admin.ModelAdmin):
    list_display = ( 'voater', 'value')

class DecisionAdmin(admin.ModelAdmin):
    list_display = ( 'content','created_at')



admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Discussion, DiscussionAdmin)

