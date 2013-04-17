from django.conf.urls import patterns, url

from cabrides import views

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    )
