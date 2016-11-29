from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'create/$', views.createform),
    url(r'enter/(?P<form_id>[0-9]+)/$', views.enterform),
    url(r'manage/(?P<form_id>[0-9]+)/$', views.manageform),
]
