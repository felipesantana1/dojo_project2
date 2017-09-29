from django.conf.urls import url
import views

urlpatterns = [

    url(r'^$', views.index),
    url(r'^wish$', views.wish),
    url(r'^wish/add$', views.addWish),
    url(r'^wish/(?P<id>\d+)$', views.display),
    url(r'^wish/add/(?P<id>\d+)$', views.addMyWish),
    url(r'^wish/delete/(?P<id>\d+)$', views.delete),
    url(r'^wish/remove/(?P<id>\d+)$', views.remove),
    url(r'^wish/create$', views.makeWish),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home)
]
