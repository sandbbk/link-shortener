from django.urls import (path, re_path)
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('signup', views.signup, name='signup'),
    re_path(r'^activate/(?P<link>[-a-z0-9]+)$', views.activate, name='activate'),
    path('stat', views.stat, name='stat'),
    path('process', views.process, name='process'),
    re_path(r'^(?P<link>[-_a-zA-Z0-9]+)$', views.follow, name='follow'),
]
