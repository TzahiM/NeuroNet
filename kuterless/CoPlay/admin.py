from CoPlay.models import Discussion, Response, Attendant
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

class AttendantAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Attendant, AttendantAdmin)

