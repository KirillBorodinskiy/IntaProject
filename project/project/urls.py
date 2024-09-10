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
    path('<int:game_id>/', views.board, name='board'),
    path('create-game/', views.create_game, name='create_game'),
    path('create-game/create-board.html/',views.create_board,name='create_board'),
    path('create-game/place-ship.html/',views.place_ship,name='place_ship'),
    path('add-ship-position/', views.add_ship_position, name="add_ship_position"),
    path("register/",views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update-cell/', views.update_game_cell, name='update_game_cell'),
]

