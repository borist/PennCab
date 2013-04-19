from django.conf.urls import patterns, url

from cabrides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.login_page, name='login'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup_user/$', views.signup_user, name='signup_user'),
    url(r'^new_ride/$', views.new_ride, name='new_ride'),
    url(r'^create_ride/$', views.create_ride, name='create_ride'),
    url(r'^(?P<ride_id>\d+)/$', views.add_rider, name='add_rider'),
    url(r'^view_user/$', views.view_user, name='view_user'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<term>[a-zA-z]+)/$', views.search_term, name='search_term'),
    )
