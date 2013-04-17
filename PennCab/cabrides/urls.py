from django.conf.urls import patterns, url

from cabrides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^(?P<ride_id>\d+)/(?P<user_id>\d+)/$', views.add_rider, name='add_rider'),
    )
