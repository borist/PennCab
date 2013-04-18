from django.conf.urls import patterns, url

from cabrides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login_page, name='login'),
    url(r'^logout/$', views.logout_user, name='logout_view'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^(?P<ride_id>\d+)/(?P<user_id>\d+)/$', views.add_rider, name='add_rider'),
    )
