from django.urls import path
from . import views

urlpatterns = [
    path('',views.top,name="top"),
    path('tag',views.tag,name="tag"),
    path('tag_search/<int:tag_id>',views.tag_search,name="tag_search"),
    path('keyword_search',views.keyword_search,name="keyword_search"),
    ]