from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'create/$',views.createForm),
	url(r'enter/(?P<id>[0-9]+)/$',views.enterForm),
	url(r'manage/(?P<id>[0-9]+)/$',views.manageForm),
]