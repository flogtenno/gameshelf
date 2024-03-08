from django.urls import path
from . import views

urlpatterns = [
    path('userpage/',views.userpage,name='userpage'),
    path('edituser/<int:user_id>',views.edituser,name='edituser'),
    path('createuser',views.createuser,name='createuser'),
    ]