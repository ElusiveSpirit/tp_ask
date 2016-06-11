from django.conf.urls import url

from ask import views as ask_views

urlpatterns = [
    url(r'^upload/', ask_views.upload, name='upload'),

    # private urls
    url(r'^ask/', ask_views.ask, name='ask'),
    url(r'^profile/edit/', ask_views.profile_detail_edit, name='profile-detail-edit'),

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
    #url(r'^', ask_views.question_list, name='index'),
]
