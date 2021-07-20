from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^studyroom/$', views.studyroom.as_view(), name='studyroom'),
    url(r'^studyroom/password/$', views.studyroom_pw.as_view(), name='studyroom_pw'),
]