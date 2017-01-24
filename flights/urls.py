from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^loggedin/$', views.loggedin, name='loggedin'),
    url(r'^logout/$', views.logout, name='logout'),
]
