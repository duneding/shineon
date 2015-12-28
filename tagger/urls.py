__author__ = 'root'

from django.conf.urls import url
from . import views

app_name = 'tagger'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    #url(r'^(?P<tweet_id>[0-9]+)/submit/$', views.SubmitView.as_view(), name='submit'),
]