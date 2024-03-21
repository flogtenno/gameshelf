from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('userpage/',views.userpage,name='userpage'),
    path('edituser',views.edituser,name='edituser'),
    path('save_edituser',views.save_edituser,name='save_edituser'),
    path('createuser',views.createuser,name='createuser'),
    path('login',views.userlogin,name='login'),
    path('logout', views.userlogout, name='logout'),
    path('deleteuser',views.deleteuser,name='deleteuser'),
    path('deleteuser_confirmation',views.deleteuser_confirmation,name='deleteuser_confirmation'),
]