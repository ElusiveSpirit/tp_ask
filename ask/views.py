import datetime
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.conf import settings

from ask.models import Tag, Profile, Question, Answer, Like
from ask.forms import AuthForm, AddQuestionForm, TestUpload, RegistrationForm, EditProfileForm, AddAnswerForm, AddLikeForm
# Create your views here.
from ask.models import TestUpload as Upload


# A paginator func for any objects lists
def get_paginator(objects, page, limit):
    try:
        limit = int(limit)
        page = int(page)
    except Exception as e:
        raise Http404("wrong parameters")

    if limit > 1000:
        limit = 1000

    paginator = Paginator(objects, limit)

    if page > paginator.num_pages:
        page = paginator.page_range[-1]

    paginator.baseurl = '/paginator/?page='
    page = paginator.page(page)
    return ( page.object_list, paginator, page )


def paginator_list(request):
    questions = Question.objects.all()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)

    questions, paginator, page = get_paginator(questions, page, limit)

    return render(request, 'ask/paginator.html', {
        'question_list' : questions,
        'paginator': paginator, 'page': page,
    })


def tag_list(request, tag):
    questions = Question.objects.by_tag(tag)

    return render(request, 'ask/question_list.html', {
        'question_list' : questions[0:10],
        'tag' : tag,
    })


class HotListView(generic.ListView):
    def get_queryset(self):
        return Question.objects.best()[0:10]

    def get_context_data(self, **kwargs):
        context = super(HotListView, self).get_context_data(**kwargs)
        context['best'] = 'True'
        return context


class QuestionListView(generic.ListView):
    def get_queryset(self):
        return Question.objects.all()[0:10]


@require_GET
def question_get_list(request):
    """
    A function for ajax requests for progressive loader
    """
    since = request.GET.get('since', 0)
    tag = request.GET.get("tag", "None")
    if tag == "":
        tag = "None"
    best = request.GET.get("best", "None")

    if tag != "None" and best == "True":
        one_year_ago = datetime.datetime.now() - datetime.timedelta(days=100)
        tag_object = Tag.objects.filter(text=tag)
        questions = Question.objects.filter(created_at__gt=one_year_ago, tags__in=tag_object).order_by('-rating', '-created_at')
    elif tag != "None":
        questions = Question.objects.byTag(tag)
    elif best == "True":
        print("best")
        questions = Question.objects.best()
    else:
        questions = Question.objects.all()

    #size = questions.count()
    #if (int(since) >= size):
    #    raise Http404("There is no so many objects yet")

    return render(request, 'ask/includes/questions.html', {
        'question_list' : questions[int(since) : int(since) + 10],
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    error = ''
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if user.is_active:
                login(request, user)
                return redirect(form.get_url())
            else:
                # Something went wrong
                pass
    else:
        form = RegistrationForm(initial={'url' : request.GET.get('next', '/')})
    return render(request, 'ask/signup.html',{
                'form' : form,
            })


def signin(request):
    login_error = False
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(form.get_url())
                else:
                    # Return a 'disabled account' error message
                    pass
        # Return an 'invalid login' error message.
        login_error = True
    else:
        form = AuthForm(initial={'url' : request.GET.get('next', '/')})
    return render(request, 'ask/signin.html',{
                'form' : form,
                'login_error' : login_error,
            })


class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(
            content = json.dumps(kwargs),
            content_type = 'application/json',
        )


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
            status = 'error', code = code, message = message
        )


def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(
                code = "no_auth",
                message = u'Требуется авторизация',
            )
        else:
            redirect('/login/?continue=' + request.get_full_path())
    return view2


@login_required_ajax
def like_question(request):
    if not request.is_ajax():
        redirect(reverse('index'))
    message = u'Unexpected error',
    #try:
    form = AddLikeForm(request.POST, profile=request.user)
    if form.is_valid():
        form.save()
        return HttpResponseAjax(
            likes = form.question.get_rating()
        )
    else:
        message = 'Invalid params'
#except:
    return HttpResponseAjaxError(
        code = 'like_error',
        message = message,
    )


def question_details(request, pk):
    """
        Here's also code for answers. Move it to another page later.
    """
    question = get_object_or_404(Question, id=pk)
    anchor = None
    if request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                content=form.cleaned_data['content'],
                author=request.user,
                question=question,
            )
            anchor = answer.get_anchor()
    else:
        form = AddAnswerForm()

    answers = Answer.objects.filter(question=question)
    return render(request, 'ask/question_detail.html', {
        'question' : question,
        'answer_list' : answers[:],
        'answer_form' : form,
        'anchor' : anchor,
    })


@login_required
def profile_detail_edit(request):
    has_changed = False
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user
            if 'username' in form.changed_data:
                profile.username = form.cleaned_data['username']
            if 'email' in form.changed_data:
                profile.email = form.cleaned_data['email']
            if 'nickname' in form.changed_data:
                profile.first_name = form.cleaned_data['nickname']
            if 'avatar' in form.changed_data:
                profile.avatar = form.cleaned_data['avatar']
            if form.has_changed():
                profile.save()
                has_changed = True
    else:
        form = EditProfileForm(initial={
            'username' : request.user.username,
            'email' : request.user.email,
            'nickname' : request.user.first_name,
        })
    return render(request, 'ask/profile_detail_edit.html', {
        'form' : form,
        # Does not work well
        # form.has_changed(),
        'saved' : has_changed
    })

@login_required
def add_question(request):
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request.user)
            return redirect(question.get_absolute_url())
    else:
        form = AddQuestionForm()
    return render(request, 'ask/ask.html', {
        'form' : form,
    })
