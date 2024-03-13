from django.urls import path
from . import views

urlpatterns = [
    path('<int:diary_id>', views.diary,name="diary"),
    path('newdiary/<int:game_id>', views.newdiary,name="newdiary"),
    path('editdiary/<int:diary_id>', views.editdiary,name="editdiary"),
    path('save_editdiary/<int:diary_id>', views.save_editdiary,name="save_editdiary"),
    path('addimagediary/<int:diary_id>', views.addimagediary,name="addimagediary"),
    path('save_addimagediary/<int:diary_id>', views.save_addimagediary,name="save_addimagediary"),
    ]