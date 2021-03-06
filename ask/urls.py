from django.conf.urls import url
from django.views.generic import ListView

from ask import views as ask_views
from ask.models import Question

urlpatterns = [
    # private urls
    url(r'^ask/', ask_views.add_question, name='ask'),
    url(r'^profile/edit/', ask_views.profile_detail_edit, name='profile-detail-edit'),
    url(r'^add_answer/', ask_views.add_answer, name='add-answer'),
    # ajax private
    url(r'^like_question/', ask_views.like_obj, {'obj' : 'question'}, name='like-question'),
    url(r'^like_answer/', ask_views.like_obj, {'obj' : 'answer'}, name='like-question'),
    url(r'^correct_answer/', ask_views.correct_answer, name='correct-answer'),

    # auth urls
    url(r'^logout/', ask_views.logout_view, name='logout'),
    url(r'^signup/', ask_views.signup, name='signup'),
    url(r'^signin/', ask_views.signin, name='signin'),

    # common urls
    url(r'^paginator/', ask_views.paginator_list, name='paginator'),
    url(r'^get_questions_list/*', ask_views.question_get_list, name='questions-get-list'),
    url(r'^hot/', ask_views.HotListView.as_view(), name='best-list'),
    url(r'^profile/(?P<pk>\d+)/$', ask_views.profile_detail.as_view(), name='profile-detail'),
    url(r'^tag_redirect/$', ask_views.tag_redirect, name='tag-redirect'),
    url(r'^tag/(?P<tag>[A-z0-9_-]+)/$', ask_views.TagList.as_view(), name='tag-list'),
    url(r'^question/(?P<pk>\d+)/(#\d+)?$', ask_views.question_details, name='question-detail'),
    url(r'^', ListView.as_view(
        queryset=Question.objects.all()[0:10]
    ), name='index'),
]
