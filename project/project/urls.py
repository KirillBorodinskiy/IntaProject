"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", auth_views.LoginView.as_view(), name='index'),

    path('create-board/', views.create_board, name='create_board'),
    path('save-board/', views.save_board, name='save-board'),
    path('connect-tables/', views.connect_tables, name='connect_tables'),
    path('update-board/', views.update_board, name='update_board'),
    path('check_for_updates/<int:game_id>/', views.check_for_updates, name='check_for_updates'),
    
    path('start-page/', views.start_page , name='start_page'),

    path('games/', views.games_view, name='games_list'),
    path('game/<int:game_id>/', views.board_view, name='game_view'),
    
    path("register/",views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name='logout'),
]

