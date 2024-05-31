from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='home'),
    path('homepage/logout', views.login_view, name='logout'),
    path('recomendations/', views.recomendations, name='reco'),

    path('vai/home', views.dashboard, name='dashboard'),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



