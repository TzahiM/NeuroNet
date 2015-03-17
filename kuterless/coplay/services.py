# -*- coding: utf-8 -*-
from coplay.control import discussion_task_email_updates, \
    task_state_change_update
from coplay.models import Task, Discussion
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string

def update_task_status_description( task_id , description, user):

    try:
        task = Task.objects.get(id=int(task_id))
    except Task.DoesNotExist:
        return False, None, 'task not found'
        
    if user is None:
        return False, None, 'no user provided'
    
    if description is None:
        return False, None, 'no description'

    if user != task.responsible:
        return False, None, 'only the responsible can update the description'

    if not task.update_status_description( description):
        return False, None, 'target date passed'
    
    task.parent.save()#verify that the entire disscusion is considered updated
    t = Template("""
    {{task.responsible.get_full_name|default:task.responsible.username}} הודיע/ה ש :\n
    "{{task.get_status_description}} "\n
    """)
    
    trunkated_subject_and_detailes = t.render(Context({"task": task}))
    
    discussion_task_email_updates(task,
                                  trunkated_subject_and_detailes,
                                  user,
                                  trunkated_subject_and_detailes)
        
    return True, task, ''



def update_task_state( task_id , new_state , user ):

    try:
        task = Task.objects.get(id=int(task_id))
    except Task.DoesNotExist:
        return False, None, 'task not found'

    if not task.parent.can_user_access_discussion( user):
        return False, None, 'user cannot access discussion'


    if user == task.responsible:
        return False, None, 'responsible can not update task status'

    if not task.set_state(new_state, user):
        return False, None, 'target date passed'
    
    task.parent.save() #verify that the entire discussion is considered updated            
    
    if new_state == task.STARTED:
        task_state_change_update( task,  u" עדיין לא השלים/ה את ")
        
    if new_state == task.ABORTED:
        task_state_change_update( task,  u" ביטל/ה את ")

    if new_state == task.CLOSED:
        task_state_change_update( task,  u" השלימ/ה את ")

    return True, task, ''


def tag_update( ModelName, id , to_add , tag):

    try:
        object = ModelName.objects.get(id)
    except ModelName.DoesNotExist:
        return None, 'not found'
    
    if to_add:
        object.tags.add( tag)
        return object, None
    object.tags.remove( tag)
    
    return object , None
        

def discussion_update( discussion_id, user, description, tags = None):

    try:
        discussion = Discussion.objects.get(id=int(discussion_id))
    except Task.DoesNotExist:
        return None, 'discussion not found'
    if user != discussion:
        return None, 'only owner can update discussion'
    
    if not discussion.is_active():
        return None, 'discussion is locked'
#         
#     discussion.description = description
#     discussion.tags.se
#     
#     
#         form.instance.description_updated_at = timezone.now()
# #         m_tags = form.cleaned_data['m_tags']  
# #         for m_tag in m_tags:
# #             form.instance.tags.add(m_tag)      
#         form.instance.save()
# 
#         
# 
#         t = Template("""
#         {{discussion.owner.get_full_name|default:discussion.owner.username}} עידכן/ה את המטרות של הפעילות והעזרה המבוקשת :\n
#         "{{discussion.description}} "\n
#         """)
#         
#         trunkated_subject_and_detailes = t.render(Context({"discussion": form.instance}))
#                                                             
#       
#         discussion_email_updates(form.instance,
#                                          trunkated_subject_and_detailes,
#                                          self.request.user,
#                                          trunkated_subject_and_detailes)
#         form.instance.start_follow(self.request.user)
#         
#         return resp


    