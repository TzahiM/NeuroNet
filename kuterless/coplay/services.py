# -*- coding: utf-8 -*-
from coplay.control import discussion_task_email_updates, \
    task_state_change_update
from coplay.models import Task
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


    