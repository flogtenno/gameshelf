from django.urls import path
from . import views

urlpatterns = [
    path('<int:game_id>', views.game,name="game"),
    path('newgame', views.newgame,name="newgame"),
    path('editgame/<int:game_id>', views.editgame,name="editgame"),
    ]