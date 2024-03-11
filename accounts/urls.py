from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('userpage/',views.userpage,name='userpage'),
    path('edituser/<int:user_id>',views.edituser,name='edituser'),
    path('createuser',views.createuser,name='createuser'),
    path('login',views.userlogin,name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]