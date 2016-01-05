__author__ = 'root'

from django.conf.urls import url
from . import views

app_name = 'tagger'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<tweet_id>[0-9]+)/$', views.SentimentView.as_view(), name='sentiment'),
    url(r'^(?P<tweet_id>[0-9]+)/save/$', views.save, name='save'),
]