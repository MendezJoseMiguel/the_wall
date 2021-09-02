from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('wall',views.wall),
    path('login',views.login),
    path('register',views.register),
    path('create_messages',views.create_messages),
    path('logout',views.logout),
]
