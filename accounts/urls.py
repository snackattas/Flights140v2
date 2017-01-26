from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^login_form/$', views.login_form,\
        name='login_form'),
    url(r'^validation_sent/$', views.validation_sent,\
        name="validation_sent"),
    url(r'^passwordless_login/(?P<token>[^/]+)/$', views.passwordless_login,\
        name='passwordless_login'),
]
