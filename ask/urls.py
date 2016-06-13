from django.conf.urls import url

from ask import views as ask_views

urlpatterns = [
    # private urls
    url(r'^ask/', ask_views.add_question, name='ask'),
    url(r'^profile/edit/', ask_views.profile_detail_edit, name='profile-detail-edit'),
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
    url(r'^tag/(?P<tag>[A-z0-9_-]+)/$', ask_views.tag_list, name='tag-list'),
    url(r'^question/(?P<pk>\d+)/(#\d+)?$', ask_views.question_details, name='question-details'),
    url(r'^', ask_views.QuestionListView.as_view(), name='index'),
]
