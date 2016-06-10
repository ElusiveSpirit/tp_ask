import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.conf import settings

from ask.models import Tag, Profile, Question, Answer, Like
from ask.forms import AuthForm, AddQuestionForm, TestUpload, RegistrationForm
# Create your views here.
from ask.models import TestUpload as Upload

def upload(request):
    if request.method == 'POST':
        form = TestUpload(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Upload(docfile = request.FILES['avatar'])
            newdoc.save()
            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = TestUpload() # A empty, unbound form
        newdoc = None


    # Render list page with the documents and the form
    return render(request,
        'ask/test_upload.html',
        {'pic': newdoc, 'form': form},
        #context_instance=RequestContext(request)
    )

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
"""
class TagListView(generic.DetailView):
    context_object_name = 'question_list'
    def get_queryset(self):
        return Question.objects.by_tag(self.get_slug_field())[0:10]

    def get_context_data(self, **kwargs):
        context = super(HotListView, self).get_context_data(**kwargs)
        context['tag'] = tag
        return context
"""

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
"""
class QuestionList(generic.ListView):

    def get(self, request, *args, **kwargs):
"""

@require_GET
def question_get_list(request):
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
    error = ''
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = form.authenticate()
            if user.is_active:
                login(request, user)
                return redirect(form.get_url())
            else:
                ...
                # Return a 'disabled account' error message
        #else:
            # Return an 'invalid login' error message.
    else:
        form = AuthForm(initial={'url' : request.GET.get('next', '/')})
    return render(request, 'ask/signin.html',{
                'form' : form,
            })


def question_details(request, pk):
    question = get_object_or_404(Question, id=pk)
    answers = Answer.objects.filter(question=question)
    return render(request, 'ask/question_detail.html', {
        'question' : question,
        'answer_list' : answers[:],
    })

@login_required
def ask(request):
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
