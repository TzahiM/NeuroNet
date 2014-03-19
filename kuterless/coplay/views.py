# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, CreateView
from coplay import models
from coplay.models import Discussion, Feedback, LikeLevel, Decision, Task
import floppyforms as forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.forms.extras.widgets import SelectDateWidget
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import generic
from django.utils.translation import ugettext as _

MAX_MESSAGE_INPUT_CHARS = 900

# Create your views here.
def root(request):
    return render(request, 'coplay/co_play_root.html', {'rtl': 'dir="rtl"'})
#hi assaf
def get_discussions_lists():
    sorted_discussions_by_inverse_locket_at_list = Discussion.objects.all().order_by(
        "-locked_at")
    sorted_discussions_by_locket_at_list = Discussion.objects.all().order_by(
        "locked_at")

    active_discussions_by_urgancy_list = []
    locked_discussions_by_relevancy_list = []

    for discussion in sorted_discussions_by_inverse_locket_at_list:
        if not discussion.is_active():
            locked_discussions_by_relevancy_list.append(discussion)

    for discussion in sorted_discussions_by_locket_at_list:
        if discussion.is_active():
            active_discussions_by_urgancy_list.append(discussion)

    return active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list

class IndexView(generic.ListView):
    model = Discussion
    template_name = 'coplay/discussion_list.html'
    context_object_name = 'latest_discussion_list'


    def get_queryset(self):
        active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()
        
        return (active_discussions_by_urgancy_list + locked_discussions_by_relevancy_list)


class AddFeedbackForm(forms.Form):
    content = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                              widget=forms.Textarea(attrs={'rows': '3'}))
    feedbabk_type = forms.ChoiceField(choices=Feedback.FEEDBACK_TYPES)


class UpdateDiscussionForm(forms.Form):
    description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea(attrs={'rows': '3'}))


class AddDecisionForm(forms.Form):
    content = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS, label='',
                              widget=forms.Textarea(attrs={'rows': '3',
                                                           'class': 'form-control'}))


class VoteForm(forms.Form):
    value = forms.ChoiceField(widget=forms.RadioSelect,
                              choices=LikeLevel.level)


class AddTaskForm(forms.Form):
    goal_description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                       label='', widget=forms.Textarea(
            attrs={'rows': '3', 'class': 'form-control'}))
    target_date = forms.DateTimeField(widget=SelectDateWidget)


class UpdateTaskForm(forms.Form):
    status_description = forms.CharField(max_length=MAX_MESSAGE_INPUT_CHARS,
                                         widget=forms.Textarea(
                                             attrs={'rows': '3'}))


def discussion_details(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return HttpResponseRedirect('coplay_root')

    list_encourage = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.ENCOURAGE).order_by("-created_at")
    list_cooperation = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.COOPERATION).order_by("-created_at")
    list_intuition = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.INTUITION).order_by("-created_at")
    list_advice = discussion.feedback_set.all().filter(
        feedbabk_type=Feedback.ADVICE).order_by("-created_at")
    list_decision = discussion.decision_set.all().order_by("-created_at")
    list_tasks = discussion.task_set.all().order_by("-target_date")
    like_levels = LikeLevel.level

    vote_form = None
    feedback_form = None
    description_form = None
    add_decision_form = None
    add_task_form = None
    if request.user.is_authenticated():
        if discussion.is_active():
            if request.user == discussion.owner:
                description_form = UpdateDiscussionForm()
                add_decision_form = AddDecisionForm()
            else:
                feedback_form = AddFeedbackForm()
                vote_form = VoteForm()

        add_task_form = AddTaskForm()

    page_name = u'עוזרים ב ' + discussion.title

    return render(request, 'coplay/discussion_detail.html',
                  {'discussion': discussion,
                   'list_encourage': list_encourage,
                   'list_cooperation': list_cooperation,
                   'list_intuition': list_intuition,
                   'list_advice': list_advice,
                   'list_decision': list_decision,
                   'list_tasks': list_tasks,
                   'feedback_form': feedback_form,
                   'description_form': description_form,
                   'add_decision_form': add_decision_form,
                   'vote_form': vote_form,
                   'add_task_form': add_task_form,
                   'like_levels': like_levels,
                   'page_name': page_name})


class NewDiscussionForm(forms.Form):
    title = forms.CharField(label=_("title"), max_length=200,
                            widget=forms.Textarea(
                                attrs={'rows': '1', 'cols': '50'}))
    description = forms.CharField(label=_("description"),
                                  max_length=MAX_MESSAGE_INPUT_CHARS,
                                  widget=forms.Textarea)


@login_required
def add_discussion(request):
    if request.method == 'POST': # If the form has been submitted...
        form = NewDiscussionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user

            discussions_list = Discussion.objects.all().filter(owner=user,
                                                               title=
                                                               form.cleaned_data[
                                                                   'title'])
            if discussions_list.count() != 0:
                return render(request, 'coplay/message.html',
                              {'message': 'כבר קיים עבורך דיון באותו נושא',
                               'rtl': 'dir="rtl"'})

            new_discussion = Discussion(owner=user,
                                        title=form.cleaned_data['title'],
                                        description=form.cleaned_data[
                                            'description'])
            new_discussion.clean()
            new_discussion.save()
            messages.success(request,
                             _("Your activity was created successfully"))
            return redirect(new_discussion)
    else:
        form = NewDiscussionForm() # An unbound form

    return render(request, 'coplay/new_discussion.html', {
        'form': form,
        'rtl': 'dir="rtl"'
    })


def send_html_message(subject, html_content, from_email, to_list):
    msg = EmailMessage(subject, html_content, from_email, to_list)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def discussion_email_updates(discussion, subject, logged_in_user):
    attending_list = discussion.get_attending_list(True)
    html_message = render_to_string("coplay/email_discussion_update.html",
                                    {'ROOT_URL': 'www.kuterless.org.il',
                                     'discussion': discussion})

    for attensdent in attending_list:
        if attensdent.email and attensdent != logged_in_user:
            send_html_message(subject, html_message,
                              'do-not-reply@kuterless.org.il',
                              [attensdent.email])


def discussion_task_email_updates(task, subject, logged_in_user):
    attending_list = task.parent.get_attending_list(True)

    html_message = render_to_string("coplay/email_task_update.html",
                                    {'ROOT_URL': 'www.kuterless.org.il',
                                     'task': task})

    for attensdent in attending_list:
        if attensdent.email and attensdent != logged_in_user:
            send_html_message(subject, html_message,
                              'do-not-reply@kuterless.org.il',
                              [attensdent.email])


@login_required
def update_discussion(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'הדיון איננו קיים',
                       'rtl': 'dir="rtl"'})

    if request.method == 'POST': # If the form has been submitted...
        form = UpdateDiscussionForm(
            request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            if user == discussion.owner:
                discussion.update_description(
                    form.cleaned_data['description'])
                discussion_email_updates(discussion,
                                         'עידכון מטרות בפעילות שבהשתתפותך',
                                         request.user)

                return HttpResponseRedirect(
                    discussion.get_absolute_url()) # Redirect after POST
            return render(request, 'coplay/message.html',
                          {'message': 'רק בעל הדיון מורשה לעדכן אותו',
                           'rtl': 'dir="rtl"'})

    return render(request, 'coplay/message.html',
                  {'message': '  לא הוזן תיאור חדש או שהוזן תיאור ארוך מדי ',
                   'rtl': 'dir="rtl"'})


@login_required
def delete_discussion(request, pk):
    try:
        discussion = Discussion.objects.get(id=int(pk))
    except Discussion.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'הדיון איננו קיים',
                       'rtl': 'dir="rtl"'})

    user = request.user
    if user == discussion.owner:
        discussion.delete()
        return HttpResponseRedirect(
            'discussions_list') # Redirect to discussions list

    return render(request, 'coplay/message.html',
                  {'message': 'רק בעל הדיון  מורשה למחוק אותו',
                   'rtl': 'dir="rtl"'})


@login_required
def add_feedback(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddFeedbackForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            if user != discussion.owner and form.cleaned_data[
                'feedbabk_type'] and form.cleaned_data['content']:
                discussion.add_feedback(user,
                                        form.cleaned_data['feedbabk_type'],
                                        form.cleaned_data['content'])
                discussion_email_updates(discussion,
                                         'התקבלה תגובה חדשה בפעילות שבהשתתפותך',
                                         request.user)

            return HttpResponseRedirect(
                discussion.get_absolute_url()) # Redirect after POST
        return render(request, 'coplay/message.html',
                      {'message': 'לא הזנת תגובה',
                       'rtl': 'dir="rtl"'})
    return HttpResponse('Request NA')


@login_required
def add_decision(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddDecisionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            user = request.user
            if user == discussion.owner:
                decisions_list = Decision.objects.all().filter(
                    content=form.cleaned_data['content'], parent=discussion)
                if decisions_list.count() != 0:
                    return render(request, 'coplay/message.html',
                                  {
                                      'message': 'כבר רשומה עבורך החלטה באותו נושא',
                                      'rtl': 'dir="rtl"'})

                discussion.add_decision(form.cleaned_data['content'])
                discussion_email_updates(discussion,
                                         'התקבלה התלבטות חדשה בפעילות שבהשתתפותך',
                                         request.user)



            else:
                return HttpResponse('Forbidden access')
            return HttpResponseRedirect(
                discussion.get_absolute_url()) # Redirect after POST
        else:
            return render(request, 'coplay/message.html',
                          {'message': 'בחר אחת מהאפשרויות',
                           'rtl': 'dir="rtl"'})
    return HttpResponseRedirect('coplay_root') # Redirect after POST


@login_required
def vote(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = VoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                decision = Decision.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return render(request, 'coplay/message.html',
                              {'message': 'משימה לא ידועה',
                               'rtl': 'dir="rtl"'})
            user = request.user
            if user != decision.parent.owner:
                decision.vote(user, int(form.cleaned_data['value']))
            return HttpResponseRedirect(
                decision.parent.get_absolute_url()) # Redirect after POST
        return render(request, 'coplay/message.html',
                      {'message': 'Please select a vote value'})

    return ( HttpResponse('Forbidden request not via form'))


@login_required
def add_task(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = AddTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            user = request.user
            try:
                discussion = Discussion.objects.get(id=int(pk))
            except Discussion.DoesNotExist:
                return HttpResponse('Discussion not found')
            target_date = form.cleaned_data['target_date']
            if target_date <= timezone.now():
                return render(request, 'coplay/message.html',
                              {'message': 'תאריך היעד חייב להיות בעתיד' + str(
                                  target_date),
                               'rtl': 'dir="rtl"'})

            tasks_list = Task.objects.all().filter(responsible=user,
                                                   goal_description=
                                                   form.cleaned_data[
                                                       'goal_description'],
                                                   parent=discussion)
            if tasks_list.count() != 0:
                return render(request, 'coplay/message.html',
                              {'message': 'כבר רשומה עבורך משימה באותו נושא',
                               'rtl': 'dir="rtl"'})

            new_task = discussion.add_task(user,
                                           form.cleaned_data[
                                               'goal_description'],
                                           form.cleaned_data['target_date'])

            discussion_task_email_updates(new_task,
                                          'נוספה משימה חדשה בפעילות שבהשתתפותך',
                                          request.user)

            return HttpResponseRedirect(
                new_task.get_absolute_url()) # Redirect after POST

    return HttpResponseRedirect('coplay_root') # Redirect after POST


def task_details(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return render(request, 'coplay/message.html',
                      {'message': 'משימה שאיננה קיימת',
                       'rtl': 'dir="rtl"'})

    close_possible = False
    update_task_form = None

    if request.user.is_authenticated():
        user = request.user
        if task.get_status() == task.STARTED:
            if user == task.responsible:
                update_task_form = UpdateTaskForm()
            else:
                close_possible = True

    return render(request, 'coplay/task_detail.html',
                  {'task': task,
                   'update_task_form': update_task_form,
                   'close_possible': close_possible,
                   'rtl': 'dir="rtl"',
                   'page_name': u'המשימה:' + task.goal_description})


@login_required
def update_task_description(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = UpdateTaskForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data# Process the data in form.cleaned_data
            try:
                task = Task.objects.get(id=int(pk))
            except Task.DoesNotExist:
                return HttpResponse('Task not found')
            user = request.user
            if user == task.responsible:
                task.update_status_description(
                    form.cleaned_data['status_description'])
                discussion_task_email_updates(task,
                                              'עודכנה משימה בפעילות שבהשתתפותך. יתכן ואפשר לסגור את המשימה',
                                              request.user)

            return HttpResponseRedirect(
                task.get_absolute_url()) # Redirect after POST

    return HttpResponseRedirect('coplay_root') # Redirect after POST


@login_required
def close_task(request, pk):
    try:
        task = Task.objects.get(id=int(pk))
    except Task.DoesNotExist:
        return HttpResponse('Task not found')
    user = request.user
    if user != task.responsible:
        task.close(user)
        discussion_task_email_updates(task, 'הושלמה משימה בפעילות שבהשתתפותך',
                                      request.user)

    return HttpResponseRedirect(task.get_absolute_url()) # Redirect after POST




def get_tasks_lists():
    for task in Task.objects.all():
        task.refresh_status()
    open_tasks_list_by_urgancy_list = Task.objects.all().filter(
        status=Task.STARTED).order_by("target_date")
    closed_tasks_list_by_relevancy_list = Task.objects.all().filter(
        status=Task.CLOSED).order_by("-closed_at")
    missed_tasks_list_by_relevancy_list = Task.objects.all().filter(
        status=Task.MISSED).order_by("-target_date")

    return open_tasks_list_by_urgancy_list, closed_tasks_list_by_relevancy_list, missed_tasks_list_by_relevancy_list


def get_user_fullname_or_username(user):
    full_name = user.get_full_name()
    if full_name:
        return full_name
    return user.username


def user_coplay_report(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse('User not found')
    else:
        user = request.user

    if user == request.user:
        page_name = u'הפעילות שלי '
    else:
        page_name = u'הפעילות של ' + get_user_fullname_or_username(user)

    open_tasks_list_by_urgancy_list, closed_tasks_list_by_relevancy_list, missed_tasks_list_by_relevancy_list = get_tasks_lists()

    active_discussions_by_urgancy_list, locked_discussions_by_relevancy_list = get_discussions_lists()

    user_s_open_tasks_list = []
    other_users_open_tasks_list = []
    missed_tasks_list = []
    user_closed_tasks_list = []

    for task in open_tasks_list_by_urgancy_list:
        if task.responsible == user:
            user_s_open_tasks_list.append(task)
        else:
            discussion = task.parent
            if user in discussion.get_attending_list(include_owner=True):
                other_users_open_tasks_list.append(task)

    for task in missed_tasks_list_by_relevancy_list:
        discussion = task.parent
        if user in discussion.get_attending_list(include_owner=True):
            missed_tasks_list.append(task)

    for task in closed_tasks_list_by_relevancy_list:
        if task.responsible == user:
            user_closed_tasks_list.append(task)

    user_discussions_active = []
    user_discussions_locked = []

    for discussion in active_discussions_by_urgancy_list:
        if user in discussion.get_attending_list(include_owner=True):
            user_discussions_active.append(discussion)

    for discussion in locked_discussions_by_relevancy_list:
        if user in discussion.get_attending_list(include_owner=True):
            user_discussions_locked.append(discussion)

    return render(request, 'coplay/coplay_report.html',
                  {
                      'tasks_open_by_increased_time_left': user_s_open_tasks_list,
                      'tasks_others_open_by_increased_time_left': other_users_open_tasks_list,
                      'discussions_active_by_increase_time_left': user_discussions_active,
                      'discussions_locked_by_increase_locked_at': user_discussions_locked,
                      'tasks_closed_by_reverse_time': user_closed_tasks_list,
                      'tasks_missed_by_reverse_time': missed_tasks_list,
                      'applicabale_user': user,
                      'page_name': page_name})


class UpdateDiscussionDescForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = (
            'description',
        )


class DiscussionOwnerView(object):
    model = Discussion

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = self.get_object()
        if self.discussion.owner != request.user:
            return HttpResponse("Unauthorized", status=401)

        return super(DiscussionOwnerView, self).dispatch(request, *args,
                                                              **kwargs)


class UpdateDiscussionDescView(DiscussionOwnerView, UpdateView):
    form_class = UpdateDiscussionDescForm


class DeleteDiscussionView(DiscussionOwnerView, DeleteView):

    model = Discussion


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'goal_description',
            'target_date',
        )
        widgets = {
            'goal_description': forms.Textarea,
            'target_date': forms.DateInput,
        }

class CreateTaskView(CreateView):
    model = Task
    form_class = CreateTaskForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        return super(CreateTaskView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        if form.instance.target_date <= timezone.now():
            return render(self.request, 'coplay/message.html',
                              {'message': 'תאריך היעד חייב להיות בעתיד' + str(
                                  form.instance.target_date),
                               'rtl': 'dir="rtl"'})
        form.instance.parent = self.discussion
        form.instance.responsible = self.request.user
        resp = super(CreateTaskView, self).form_valid(form)
        form.instance.parent.unlock()
        discussion_task_email_updates(form.instance,
                                          'נוספה משימה חדשה בפעילות שבהשתתפותך',
                                          self.request.user)
        return resp


class CreateFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            'feedbabk_type',
            'content',
        )
        widgets = {
            'content': forms.Textarea,
            'feedbabk_type': forms.Select,
        }



class CreateFeedbackView(CreateView):
    model = Feedback
    form_class = CreateFeedbackForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        return super(CreateFeedbackView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        form.instance.discussion = self.discussion
        form.instance.user = self.request.user
        resp = super(CreateFeedbackView, self).form_valid(form)        
        discussion_email_updates(form.instance.discussion,
                                         'התקבלה תגובה חדשה בפעילות שבהשתתפותך',
                                         self.request.user)
        return resp


class CreateDecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = (
            'content',
        )
        widgets = {
            'content': forms.Textarea,
        }



class CreateDecisionView(CreateView):
    model = Decision
    form_class = CreateDecisionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        if self.discussion.owner != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super(CreateDecisionView, self).dispatch(request, *args,
                                                              **kwargs)

    def form_valid(self, form):
        form.instance.parent = self.discussion
        resp = super(CreateDecisionView, self).form_valid(form)
        # form.instance is the new decision
        discussion_email_updates(form.instance.parent,
                                         'התקבלה התלבטות חדשה בפעילות שבהשתתפותך',
                                         self.request.user)
        
        
        return resp



