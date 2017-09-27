from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.home),
    url(r'^logout$', views.logout),
    url(r'^books/add$', views.create),
    url(r'^books/(?P<id>\d+)$', views.showbook),
    url(r'^users/(?P<id>\d+)$', views.showuser),
    url(r'^books/users/(?P<id>\d+)$', views.showuser),
    url(r'^destroy/(?P<id>\d+)$', views.destroy),
]