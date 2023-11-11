from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import include, path

urlpatterns = [
    path('signup/', views.enter_email, name='enter_email'),
    path('signup/step2/', views.register_user, name='register_user'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='logout'),
    path('information', views.information, name = 'information'),
    path('edit', views.edit, name = 'edit'),
    path('', include('music.urls')),
    path('resetpassword', views.reset_password, name = 'rpass'),
    path('reset/<uidb64>/<token>', views.reset, name='reset'),

]
