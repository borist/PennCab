from django.conf.urls import patterns, url

from cabrides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login_page, name='login'),
    url(r'^navbar_item/$', views.navbar_item, name='navbar_item'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^new_ride/$', views.new_ride, name='new_ride'),
    url(r'^create_ride/$', views.create_ride, name='create_ride'),
    url(r'^(?P<ride_id>\d+)/$', views.add_rider, name='add_rider'),
    )
