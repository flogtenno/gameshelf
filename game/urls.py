from django.urls import path
from . import views

urlpatterns = [
    path('<int:game_id>', views.game,name="game"),
    path('newgame', views.newgame,name="newgame"),

    ]